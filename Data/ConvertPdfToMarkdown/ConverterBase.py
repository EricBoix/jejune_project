import re
from typing import Callable

# To deal with inputs of the Converter class
from pypdf import PdfReader

# To deal with outputs of the Converter class
from .Model import (
    DocumentHierarchicalLevel,
    ChapterOfParagraphs,
    SuperChapter,
    Paragraph,
    Sentence,
    TopLevelChapter,
)
from .PageLayout import PageLayout
from .Warning import Warning, WarnAndExit
from .Traces import Debug

# To realize the conversion per se
import nltk

# Refer to
# https://stackoverflow.com/questions/78862426/unable-to-use-nltk-functions
nltk.download("punkt_tab", quiet=True)


class ConverterBase:
    """
    Class converting the original set of pages extracted from the pypdf::reader
    to a structured document. In order to realize its purpose the Converter
    needs to be manually provided with the structural information (extracted by
    a human reader) that must be promoted to the semantic structure (document,
    chapter, sub-chapter, paragraph...).
    """

    def __init__(self, pdf_filename, document, structural_info):

        # The original pdf document file name that this converter will act from
        self.pdf_filename = pdf_filename

        # The structural information constituted by the presence of chapters,
        # illustrations ... is quite often difficult to be automatically
        # discovered. While waiting for better (and free) tools, the following
        # was manually extracted
        self.structural_info = structural_info

        # The result of the conversion process
        self.document = document

        # Parse the pdf and make some basic coherence checks on the result:
        self.reader = PdfReader(self.pdf_filename)
        if len(self.reader.pages) != self.structural_info.total_page_number:
            WarnAndExit(
                f"Erroneous number of pages: was expecting {self.structural_info.total_page_number} but got {len(self.reader.pages)}"
            )
        for page_number in range(self.structural_info.total_page_number):
            self._assert_reader_page_number_is_coherent(page_number)

        # Eventually realize the conversion
        self.build_document()

    def is_chapter_beginning_page(self, extracted_page):
        # By default we can only assume some structural information, since we
        # don't know wether ExtractedPage will be specialized or not.
        return self.structural_info._is_chapter_beginning_page(
            extracted_page.page_number
        )

    def get_chapter_name(self, extracted_page):
        # By default we can only assume some structural information, since we
        # don't know whether ExtractedPage will be specialized or not.
        return self.structural_info._get_chapter_name(extracted_page.page_number)

    def get_chapter_extracted_page(self, extracted_page):
        """Get the extracted page of the chapter holding the given extracted page."""
        chapter_page_number = self.structural_info._get_chapter_page_number(
            extracted_page.page_number
        )
        chapter_extracted_page = self.document.get_chapter_extracted_page(
            chapter_page_number
        )
        if not chapter_extracted_page:
            WarnAndExit(
                f"Chapter for page number {extracted_page.page_number} not found."
            )
        return chapter_extracted_page

    def breaks_document_into_chapters(self, ExtractedPageDerived, ChapterDerived):
        current_chapter = None
        for page_number in range(0, self.structural_info.total_page_number):

            if self.structural_info._page_is_dropped(page_number):
                continue

            ### Create a new extracted page:
            new_extracted_page_layout = PageLayout(
                self.structural_info.convert_to_logical_page_number(page_number),
                page_number,
            )
            new_extracted_page_layout.set_reference_text(
                f"[Page: {new_extracted_page_layout.reader_page_number} (page number: {new_extracted_page_layout.page_number})]"
            )
            # The usage of ExtractedPage, that can be a derived class, prevents
            # the declaration of this member function to be done in the parent
            # class. This is because although all derived classes with define
            # exactly the same function definition, the concrete ExtractedPage
            # class type might (and thus will) differ from one derivation of
            # a converter to another one.
            new_extracted_page = ExtractedPageDerived(
                page_number,
                new_extracted_page_layout,
                self.reader.pages[page_number],  # Original page
            )

            if not self.is_chapter_beginning_page(new_extracted_page):
                # When the new extracted page is not the beginning of a chapter
                # we must still assert that the current_chapter was previously
                #  encountered
                if not current_chapter:
                    # We didn't encounter a first chapter yet the first
                    # encountered page is not a page starting a chapter.
                    # Something went really wrong.
                    WarnAndExit(
                        f"Any chapter must start with...a chapter typed page.\nNote: we didn't encounter the first chapter yet.\nThis was the content of the extracted page: {new_extracted_page}"
                    )
                self.structural_info.set_chapter_page_number(
                    new_extracted_page.page_number,
                    current_chapter.page_layout.page_number,
                )
            else:
                # This new extracted page is the one of a new chapter. We must
                # thus create it (a Chapter object) as such and define this new
                # Chapter as the current_chapter:
                self.structural_info.set_chapter_page_number(
                    new_extracted_page.page_number,
                    new_extracted_page.page_number,
                )
                new_chapter_name = self.get_chapter_name(new_extracted_page)
                if new_chapter_name is None:
                    WarnAndExit(
                        f"This looks like a new chapter yet it has no name.\nThis was the content of the extracted page: {new_extracted_page}"
                    )

                # Some chapter names include newline characters that must be
                # sanitized in order to create a proper new Chapter object:
                sanitized_new_chapter_name = re.sub("\n", " ", new_chapter_name)
                current_chapter = ChapterDerived(sanitized_new_chapter_name)
                self.document.add_chapter(current_chapter)
                # Yet what we must extracted is the "un-sanitized" chapter name
                new_extracted_page.extract_chapter_name(new_chapter_name)

            # We are back to the default flow of treatment
            self.sanitize_page_text(new_extracted_page)  # In derived class
            self.fix_typos(new_extracted_page)
            current_chapter.add_page(new_extracted_page)

    def fix_typos(self, extracted_page):
        """Apply typo fixes on extracted pages that require it."""
        page_number = extracted_page.page_number
        typo_and_fix = self.structural_info.get_typo_and_fix(page_number)
        if typo_and_fix is None:
            return
        typo = typo_and_fix["typo"]
        if not re.search(typo, extracted_page.text):
            Warning(f"Couldn't find typo in extracted page number {page_number}:")
            Warning(f"  - typo: {typo}")
            Warning(f"  - page text: {extracted_page.text}")
            return
        extracted_page.text = re.sub(typo, typo_and_fix["fix"], extracted_page.text)
        Debug(f"Typo fixed on page {page_number}")

    def _assert_reader_page_number_is_coherent(self, page_number):
        # Slightly paranoid check on the reader numbering job coherence. When
        # given a page_number assert that the corresponding page wears that
        # very same page number (pretty dumb test BTW)
        original_reader_page = self.reader.pages[page_number]
        original_reader_page_number = self.reader.get_page_number(original_reader_page)
        if page_number != original_reader_page_number:
            Warning(
                f"Python page number does not match pypdf::reader page number:\n   - Python page number:  {page_number}\n   - pypdf::reader page number: {original_reader_page_number}"
            )
        return True

    def _page_requires_paragraph_continuation(self, page_number):
        if not page_number in self.structural_info.pages_info:
            return True  # Looks a bit ambitious but let's try it
        if "paragraph_fits_on_page" in self.structural_info.pages_info[page_number]:
            return False
        return True

    def _chapter_get_first_paragraph_of_given_page(self, chapter, page_number):
        for sublevel in chapter.get_sublevels():
            if isinstance(sublevel, ChapterOfParagraphs):
                # We just need to recuse:
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

    def _chapter_get_last_paragraph_of_given_page(self, chapter, page_number):
        sublevel_of_that_page = None
        for sublevel in chapter.get_sublevels():
            if isinstance(sublevel, ChapterOfParagraphs):
                # We just need to recuse:
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

    def sanitize_newlines_and_multiple_whitespaces(self, input_text):

        # Newlines are encountered to denote different usages
        #  - set some tabulations of illuminations (example "\       ")
        #  - define a new paragraph in which case newline is followed by
        #    exactly 4 whitespaces (example "\n    "): refer to
        #    break_chapter_into_paragraphs() method
        #  - simple line folding within original paragraphs or even sentences
        #    were newline are used to format the original pdf with lines returns.
        # Remove such formatting characters to preserve only the text content:
        result = re.sub("\n", " ", input_text)

        # The above clean-up might create multiple whitespaces, while some
        # other occurrences of multiple whitespaces are (randomly?) encountered.
        # Remove them all:
        result = re.sub(r"\s+", " ", result).strip()
        return result

    def build_document(self):
        """
        Build the Document object out of converter extracted chapters
        """
        self.breaks_document_into_chapters()  # Calling the derived version
        for chapter in self.document.get_chapters():
            self.break_level(chapter)
        for top_level_chapter in self.document.get_chapters():
            self.reconstitute_paragraphs_spreading_over_two_pages(top_level_chapter)

    def get_document(self):
        return self.document

    def break_paragraph_into_sentences(self, paragraph: Paragraph):
        paragraph_layout = paragraph.page_layout

        # Using the text attribute that was piggybacked from the above
        # break_chapter_into_paragraphs() method:
        if paragraph.text is None:
            WarnAndExit(
                "Error: trying to break a paragraph into sentences but "
                "the paragraph text is None."
            )
        paragraph_text = paragraph.text
        tokenized_text = nltk.tokenize.sent_tokenize(paragraph_text)
        for new_sentence_text in tokenized_text:
            if len(new_sentence_text) == 0:
                # Avoid creating empty sentences (resulting from previous
                # erroneous/careless string manipulations):
                continue

            # Eventually, create a new sentence
            new_sentence_layout = paragraph_layout.__copy__()
            new_sentence_layout.set_reference_text(
                "[Sentence: on reader page number: "
                + str(paragraph_layout.reader_page_number)
                + " within "
                + paragraph_layout.reference_text
                + "]"
            )
            new_sentence_text = self.sanitize_newlines_and_multiple_whitespaces(
                new_sentence_text
            )
            new_sentence = Sentence(new_sentence_text, new_sentence_layout)
            paragraph.add_sentence(new_sentence)

    def _try_create_sublevel(
        self, level, sublevel_factory, new_layout, parts, level_splitter
    ):
        """Try to create a sublevel from parts[0] (name) and parts[1] (content).
        Returns the new sublevel if created, None otherwise."""
        if len(parts) < 2:
            return None
        new_sublevel_name = level_splitter.get_sublevel_name(parts[0])
        if not new_sublevel_name:
            return None
        new_sublevel = sublevel_factory(new_layout)
        new_sublevel.set_name(new_sublevel_name)
        new_sublevel.append_text(parts[1])
        self.break_level(new_sublevel)
        del parts[0]
        del parts[0]
        level.add_sublevel(new_sublevel)
        return new_sublevel

    def _handle_unbreakable_text(
        self, parts, sublevel_factory, new_layout, current_level
    ):
        """Handle text that cannot be broken into sublevels.
        Returns: 'break' to exit while loop, 'continue' to continue, None otherwise."""
        new_sublevel_type = type(sublevel_factory(None))

        if new_sublevel_type == Paragraph:
            new_paragraph = Paragraph(new_layout)
            new_paragraph.append_text(parts[0])
            self.break_level(new_paragraph)
            current_level.add_sublevel(new_paragraph)
            if len(parts) == 1:
                parts.clear()
            else:
                del parts[0]
            return "continue"

        if new_sublevel_type == ChapterOfParagraphs:
            # Create a Paragraph directly in the SuperChapter instead of
            # a ChapterOfParagraphs containing a single paragraph.
            class ParagraphContent:
                pass

            ParagraphContent.page_layout = new_layout
            ParagraphContent.text = parts[0]
            self.break_any_level_chapter_into_paragraphs(
                current_level, [ParagraphContent]
            )
            if len(parts) == 1:
                parts.clear()
                return "break"
            del parts[0]
            return "continue"

        WarnAndExit(
            f"Expected Paragraph or ChapterOfParagraphs, got {new_sublevel_type}"
        )
        return None

    def break_level_into_sublevels(
        self,
        level: DocumentHierarchicalLevel,
        level_splitter,
        sublevel_factory: Callable[[PageLayout], DocumentHierarchicalLevel],
        reference_prefix: str,
        contents=None,
    ) -> None:
        """Break a hierarchical level into sublevels using the provided splitter."""
        Debug(f"########### break_level_into_sublevels, level: {level}")

        if not contents:
            contents = level.get_text_with_layout()
            if not contents:
                Warning(f"DocumentHierarchicalLevel {level} with NO text content.")

        current_level = level
        for level_content in contents:
            content_text = level_content.text
            Debug(f"####### break_level_into_sublevels, contents: {content_text}")
            if not content_text:
                Warning(f"level with NO text in {reference_prefix}.")
                continue

            content_layout = level_content.page_layout
            new_layout = content_layout.__copy__()
            new_layout.set_reference_text(
                f"[{reference_prefix}: {current_level.name}, "
                f"reader page number: {content_layout.reader_page_number}, "
                f"page number: {content_layout.page_number}]"
            )

            parts = level_splitter.split(content_text)
            while parts:
                Debug(f"### break_level_into_sublevels, ({len(parts)}) parts: {parts}")

                new_sublevel = self._try_create_sublevel(
                    level, sublevel_factory, new_layout, parts, level_splitter
                )
                if new_sublevel:
                    current_level = new_sublevel
                    continue

                action = self._handle_unbreakable_text(
                    parts, sublevel_factory, new_layout, current_level
                )
                if action == "break":
                    break
                if action == "continue":
                    continue

    def break_any_level_chapter_into_paragraphs(self, chapter, contents=None) -> None:
        """The chapter argument can be of any level e.g. a SuperChapter or a ChapterOfParagraphs..."""
        self.break_level_into_sublevels(
            level=chapter,
            level_splitter=self.structural_info.chapter_to_paragraph_splitter(),
            sublevel_factory=Paragraph,
            reference_prefix="Chapter",
            contents=contents,
        )
        chapter.renumber_paragraphs()

    def break_superchapter_into_chapters(self, chapter: SuperChapter) -> None:
        def chapter_of_paragraph_factory(layout: PageLayout) -> ChapterOfParagraphs:
            chapter_of_paragraph = ChapterOfParagraphs("")
            chapter_of_paragraph.page_layout = layout
            return chapter_of_paragraph

        self.break_level_into_sublevels(
            level=chapter,
            level_splitter=self.structural_info.superchapter_to_chapter_splitter(),
            sublevel_factory=chapter_of_paragraph_factory,
            reference_prefix="Sub-Chapter",
        )
        chapter.renumber_chapters()

    def break_level(self, level):
        LEVEL_HANDLERS = {
            Paragraph: self.break_paragraph_into_sentences,
            ChapterOfParagraphs: self.break_any_level_chapter_into_paragraphs,
            SuperChapter: self.break_superchapter_into_chapters,
        }
        handler = LEVEL_HANDLERS.get(type(level))
        if handler:
            handler(level)
            return
        WarnAndExit(f"Level of type {type(level)} has no break handler.")

    def break_sublevels(self, level):
        """Assuming this level was already broken into sublevels, recurse the breaking on its sublevels"""
        sublevels = level.get_sublevels()
        if not sublevels:
            WarnAndExit("Level without sublevels. Nothing to be done.")
            return
        for sublevel in sublevels:
            self.break_level(sublevel)

    def reconstitute_paragraphs_spreading_over_two_pages(self, top_level_chapter):
        """
        When a page ends with an unfinished Paragraph then the next page begins
        with the end of that Paragraph. In order to reconstitute such Paragraphs
        that were split in two, we need to
         - find the last Paragraph of a page that is not annotated with the
           "paragraph_fits_on_page" flag. Such a Paragraph holds the beginning
            of an original paragraph that got split in two.
         - the next Paragraph thus holds the end of the original paragraph
           (that got split in two) and
           - was standing at the top of the next page
           - contains a paragraph delimiter.
         - merge those two paragraphs into a single Paragraph
         - when doing so make sure that the sentence that got split (and was
           standing over two ill reconstituted Paragraphs) gets also properly
           reconstituted.
        """
        # Design notes: by segmenting the reconstitution by TopLevelChapters
        # (two paragraphs belonging to two different TopLevelChapters will
        # never be merged) the assumptions are
        # - TopLevelChapters never have a page in common
        # - SubChapters do sometimes lie over two pages and can thus have
        #   paragraphs that require to be merged
        if not isinstance(top_level_chapter, TopLevelChapter):
            return

        if len(top_level_chapter.pages) == 1:
            # Nothing to do for a single page
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
            if self.structural_info._is_chapter_beginning_page(next_page_number):
                # The next page is the starting page of a new
                # top_level_chapter. This implies that the current page is the
                # last page of this top_level_chapter which is thus complete.
                # There is hence nothing to be collected from the next page
                continue

            ill_starting_paragraph = self._chapter_get_first_paragraph_of_given_page(
                top_level_chapter, next_page_number
            )
            if ill_starting_paragraph is None:
                # The current page has no paragraph. One of the reasons for
                # a page without paragraphs can be that
                # - initially the page had a paragraph (that was ill starting)
                # - this paragraph got merged with the ill-ending paragraph
                #   of its previous
                # - as a consequence the paragraph of the page was moved away
                #   to end up with its previous paragraphs (actually it ended
                #   up merged into its previous page last paragraph)
                # - hence the page ended up with no paragraph at all
                continue
            if not isinstance(ill_starting_paragraph, Paragraph):
                Warning("Ill starting paragraph is not ... a paragraph.")
                Warning("Not merging.")
                continue

            ill_ending_paragraph = self._chapter_get_last_paragraph_of_given_page(
                top_level_chapter, page_number
            )
            if ill_ending_paragraph is None:
                # The next page has no paragraph. Besides the reason given
                # above for encountering a page without paragraphs, it can
                # also happen that the page initial paragraphs got dropped
                # during the sanitation process. Anyhow, if there is no
                # possible end for the paragraph, then there is nothing to
                # merge...
                continue
            if not isinstance(ill_ending_paragraph, Paragraph):
                Warning("Ill ending paragraph is not ... a paragraph.")
                Warning("Not merging.")
                continue
            if not ill_ending_paragraph.get_sentences():
                # This paragraph is devoid of sentence content. Nothing can
                # be merged
                continue

            #### Asserting some preconditions before merging the two paragraphs:

            # Assert that the page_layout of the two paragraphs do differ
            if ill_ending_paragraph.page_layout == ill_starting_paragraph.page_layout:
                WarnAndExit(
                    f"Error: the page layout of the two paragraphs to be merged is the same. This is not expected.\nParagraph ending on page number {page_number} has page layout {repr(ill_ending_paragraph.page_layout)}\nParagraph starting on page number {next_page_number} has page layout {repr(ill_starting_paragraph.page_layout)}"
                )

            # At least the types of parents of ill_ending and ill_starting
            # paragraphs should be of the same type. Otherwise we are crossing # some boundary.
            if type(ill_starting_paragraph._owning_hierarchical_level) != type(
                ill_ending_paragraph._owning_hierarchical_level
            ):
                # We should inquire further but we are probably in the case
                # where:
                #  - self and other are both paragraphs
                #  - type(parent(self)) is a SuperChapter
                #  - type(parent(other)) is a ChapterOfParagraph (that belongs
                #    to the same SuperChapter)
                # Although the paragraphs follow themselves, they do not share
                # the same parent (but maybe the same grand-parent).
                Warning(
                    f"Choosing not to merge {ill_starting_paragraph} and {ill_ending_paragraph}, because"
                )
                Warning(f"their respective parents are of different types: ")
                Warning(
                    f"which are respectively {type(ill_starting_paragraph._owning_hierarchical_level)} and {type(ill_ending_paragraph._owning_hierarchical_level)}."
                )
                continue

            # Not having the same hierarchical parent also means crossing
            # a chapter boundary. We can see no good reasons to do so.
            if (
                ill_starting_paragraph._owning_hierarchical_level
                != ill_ending_paragraph._owning_hierarchical_level
            ):
                Warning(
                    f"Choosing not to merge {ill_starting_paragraph} from page {ill_starting_paragraph.page_layout.page_number} and {ill_ending_paragraph} from page {ill_ending_paragraph.page_layout.page_number}, because they are not siblings."
                )
                continue

            #### Proceed with the merging of two paragraphs into a single one:
            first_sentence_of_ill_starting_paragraph = (
                ill_starting_paragraph.get_sentences()[0]
            )
            last_sentence_of_ill_ending_paragraph = (
                ill_ending_paragraph.get_sentences()[-1]
            )
            if last_sentence_of_ill_ending_paragraph.is_complete():
                # Being complete, let's assume there is nothing to be done
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
