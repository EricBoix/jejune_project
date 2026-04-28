from .Model import (
    TopLevelChapterOfParagraphs,
    SubChapterOfParagraphs,
    Paragraph,
    Sentence,
    TopLevelChapter,
)
from .Warning import Warning, WarnAndExit


class ParagraphMerger:
    """Handles merging of paragraphs that span across page boundaries."""

    def __init__(self, structural_info):
        self.structural_info = structural_info

    def _page_requires_paragraph_continuation(self, page_number: int) -> bool:
        if page_number not in self.structural_info.pages_info:
            return True  # Looks a bit ambitious but let's try it
        if "paragraph_fits_on_page" in self.structural_info.pages_info[page_number]:
            return False
        return True

    def _chapter_get_first_paragraph_of_given_page(self, chapter, page_number: int):
        for sublevel in chapter.get_sublevels():
            if isinstance(sublevel, (TopLevelChapterOfParagraphs, SubChapterOfParagraphs)):
                sublevel_result = self._chapter_get_first_paragraph_of_given_page(
                    sublevel, page_number
                )
                if sublevel_result is None:
                    continue
                return sublevel_result
            if isinstance(sublevel, Sentence):
                WarnAndExit("We should have crossed a Paragraph before.")
            if isinstance(sublevel, Paragraph):
                if sublevel.has_page_number(page_number):
                    return sublevel
        Warning(f"Paragraph of {chapter} with page number {page_number} not found.")
        return None

    def _chapter_get_last_paragraph_of_given_page(self, chapter, page_number: int):
        sublevel_of_that_page = None
        for sublevel in chapter.get_sublevels():
            if isinstance(sublevel, (TopLevelChapterOfParagraphs, SubChapterOfParagraphs)):
                result = self._chapter_get_last_paragraph_of_given_page(
                    sublevel, page_number
                )
                if result is not None and result.has_page_number(page_number):
                    sublevel_of_that_page = result
                    continue
            if isinstance(sublevel, Sentence):
                WarnAndExit("We should have crossed a Paragraph before.")
            if isinstance(sublevel, Paragraph):
                if sublevel.has_page_number(page_number):
                    sublevel_of_that_page = sublevel
        return sublevel_of_that_page

    def reconstitute_paragraphs_spreading_over_two_pages(self, top_level_chapter):
        """Merge paragraphs that were split across page boundaries.

        When a page ends with an unfinished Paragraph then the next page begins
        with the end of that Paragraph. In order to reconstitute such Paragraphs
        that were split in two, we need to:
        - find the last Paragraph of a page that is not annotated with the
          "paragraph_fits_on_page" flag
        - the next Paragraph holds the end of the original paragraph
        - merge those two paragraphs into a single Paragraph
        - when doing so make sure that the sentence that got split gets also
          properly reconstituted
        """
        if not isinstance(top_level_chapter, TopLevelChapter):
            return

        if len(top_level_chapter.pages) == 1:
            return

        for page_index in range(0, len(top_level_chapter.pages) - 1):
            current_page = top_level_chapter.pages[page_index]
            page_number = current_page.page_number
            if not self._page_requires_paragraph_continuation(page_number):
                continue
            next_page_number = (
                self.structural_info._get_page_number_finishing_last_paragraph(
                    page_number
                )
            )
            if self.structural_info._holds_new_chapter(next_page_number):
                continue

            ill_starting_paragraph = self._chapter_get_first_paragraph_of_given_page(
                top_level_chapter, next_page_number
            )
            if ill_starting_paragraph is None:
                continue
            if not isinstance(ill_starting_paragraph, Paragraph):
                Warning("Ill starting paragraph is not ... a paragraph.")
                Warning("Not merging.")
                continue

            ill_ending_paragraph = self._chapter_get_last_paragraph_of_given_page(
                top_level_chapter, page_number
            )
            if ill_ending_paragraph is None:
                continue
            if not isinstance(ill_ending_paragraph, Paragraph):
                Warning("Ill ending paragraph is not ... a paragraph.")
                Warning("Not merging.")
                continue
            if not ill_ending_paragraph.get_sentences():
                continue

            # Assert that the page_layout of the two paragraphs do differ
            if ill_ending_paragraph.page_layout == ill_starting_paragraph.page_layout:
                WarnAndExit(
                    f"Error: the page layout of the two paragraphs to be merged is the same. This is not expected.\nParagraph ending on page number {page_number} has page layout {repr(ill_ending_paragraph.page_layout)}\nParagraph starting on page number {next_page_number} has page layout {repr(ill_starting_paragraph.page_layout)}"
                )

            # Check parent types match
            if type(ill_starting_paragraph._owning_hierarchical_level) is not type(
                ill_ending_paragraph._owning_hierarchical_level
            ):
                Warning(
                    f"Choosing not to merge {ill_starting_paragraph} and {ill_ending_paragraph}, because"
                )
                Warning("their respective parents are of different types: ")
                Warning(
                    f"which are respectively {type(ill_starting_paragraph._owning_hierarchical_level)} and {type(ill_ending_paragraph._owning_hierarchical_level)}."
                )
                continue

            # Check same hierarchical parent
            if (
                ill_starting_paragraph._owning_hierarchical_level
                != ill_ending_paragraph._owning_hierarchical_level
            ):
                Warning(
                    f"Choosing not to merge {ill_starting_paragraph} from page {ill_starting_paragraph.page_layout.page_number} and {ill_ending_paragraph} from page {ill_ending_paragraph.page_layout.page_number}, because they are not siblings."
                )
                continue

            # Proceed with the merging
            first_sentence_of_ill_starting_paragraph = (
                ill_starting_paragraph.get_sentences()[0]
            )
            last_sentence_of_ill_ending_paragraph = (
                ill_ending_paragraph.get_sentences()[-1]
            )
            if last_sentence_of_ill_ending_paragraph.is_complete():
                continue
            # First merge the two sentences:
            last_sentence_of_ill_ending_paragraph.append(
                first_sentence_of_ill_starting_paragraph
            )
            ill_starting_paragraph.remove_sentence(
                first_sentence_of_ill_starting_paragraph
            )
            # Then merge the two paragraphs:
            ill_ending_paragraph.merge(ill_starting_paragraph)
