import sys
import re
import os

sys.path.append(os.path.join("..", "..", "..", "ConvertPdfToMarkdown"))
from ConverterBase import ConverterBase
from Model import Chapter
from PageLayout import PageLayout
from ExtractedPage import ExtractedPage


class Converter(ConverterBase):
    """
    Converter for The Mind Illuminated book.
    """

    def __init__(self, pdf_filename, structural_info):
        super().__init__(
            pdf_filename,
            structural_info,
            "The MIND ILLUMINATED: A Complete Meditation Guide Integrating Buddhist Wisdom and Brain Science for Greater Mindfulness",
        )

    def _convert_to_logical_page_number(self, page_number):
        if page_number == 0:
            return "Cover"
        # Just making sure
        original_reader_page = self.reader.pages[page_number]
        original_reader_page_number = self.reader.get_page_number(original_reader_page)
        if page_number != original_reader_page_number:
            print("Python page number does not match pypdf::reader page number:")
            print("   - Python page number: ", page_number)
            print("   - pypdf::reader page number: ", original_reader_page_number)
            print("Exiting.")
            sys.exit()
        return page_number

    def _get_page_number_finishing_last_paragraph(self, page_number):
        """
        A page that is followed by an illustration will need to skip that
        illustration page in order to retrieve the end of its last paragraph.
        Return the page number of the first page that defines a paragraph
        delimiter.
        """
        next_page_number = page_number + 1
        while self._page_is_illustration(next_page_number):
            print(
                "Skipping illustration of page number ",
                next_page_number,
                " while looking for the content of the end of the paragraph",
            )
            print("that starts on page number  ", page_number, ".")
            next_page_number += 1
        return next_page_number

    def reconstitute_paragraphs_spreading_over_two_pages(self, chapter):
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
        if len(chapter.pages) == 1:
            # Nothing to do for a single page
            return
        for page_index in range(0, len(chapter.pages) - 1):
            current_page = chapter.pages[page_index]
            page_number = current_page.page_number
            if not self._page_requires_paragraph_continuation(page_number):
                continue
            next_page_number = self._get_page_number_finishing_last_paragraph(
                page_number
            )
            if self._is_chapter_beginning_page(next_page_number):
                # The next page is the starting page of a new chapter. This
                # implies that the current page is the last page of this
                # chapter which is thus complete. There is hence nothing to be
                # collected from the next page
                continue

            ill_ending_paragraph = self._chapter_get_last_paragraph_of_given_page(
                chapter, page_number
            )
            ill_starting_paragraph = self._chapter_get_first_paragraph_of_given_page(
                chapter, next_page_number
            )

            #### Asserting some preconditions before merging the two paragraphs:

            # Assert that the page_layout of the two paragraphs do differ
            if ill_ending_paragraph.page_layout == ill_starting_paragraph.page_layout:
                print(
                    "Error: the page layout of the two paragraphs to be merged is the same.",
                    "This is not expected.",
                )
                print(
                    "Paragraph ending on page number ",
                    page_number,
                    " has page layout ",
                    repr(ill_ending_paragraph.page_layout),
                )
                print(
                    "Paragraph starting on page number ",
                    next_page_number,
                    " has page layout ",
                    repr(ill_starting_paragraph.page_layout),
                )
                print("Exiting.")
                sys.exit()

            #### Proceed with the merging of two paragraphs into a single one:
            first_sentence_of_ill_starting_paragraph = ill_starting_paragraph.sentences[
                0
            ]
            last_sentence_of_ill_ending_paragraph = ill_ending_paragraph.sentences[-1]
            # First merge the two sentences:
            last_sentence_of_ill_ending_paragraph.append(
                first_sentence_of_ill_starting_paragraph
            )
            ill_starting_paragraph.remove_sentence(
                first_sentence_of_ill_starting_paragraph
            )
            # Then merge the two paragraphs:
            ill_ending_paragraph.merge(ill_starting_paragraph)

    def define_sanitized_text(self, extracted_page):
        """
        After extraction of the text from the original pdf, some ad hoc
        manual cleaning is alas required.
        """
        original_page_text = extracted_page.original_pdf_page.extract_text(
            extraction_mode="layout"
        )

        # For some undocumented reason the pdfreader output has "\t" characters
        # instead of whitespaces. Brutally convert those tabulations to
        # whitespaces
        sanitized_page_text = re.sub("\\t", " ", original_page_text)

        # Remove the heading bunch of whitespaces (and assimilated characters)
        sanitized_page_text = sanitized_page_text.lstrip()

        extracted_page.text = sanitized_page_text

    def build_chapters(self):
        resulting_chapters = []
        current_chapter = None
        for page_number in range(0, self.structural_info.total_page_number):

            if self._page_is_dropped(page_number):
                continue

            if self._is_chapter_beginning_page(page_number):
                new_chapter_name = self._get_chapter_name(page_number)
                current_chapter = Chapter(new_chapter_name)
                resulting_chapters.append(current_chapter)
            else:
                if not current_chapter:
                    # We didn't encounter a first chapter yet the first
                    # encountered page is not a page starting a chapter.
                    print("Any chapter must start with...a chapter typed page.")
                    print("Note: we didn't encounter the first chapter yet.")
                    print("Exiting")
                    sys.exit()

            ### Create a new extracted page:
            new_extracted_page_layout = PageLayout(
                self._convert_to_logical_page_number(page_number), page_number
            )
            new_extracted_page_layout.set_reference_text(
                "[Page: "
                + str(new_extracted_page_layout.reader_page_number)
                + " (page number: "
                + str(new_extracted_page_layout.page_number)
                + ")]"
            )
            new_extracted_page = ExtractedPage(
                page_number,
                new_extracted_page_layout,
                self.reader.pages[page_number],  # Original page
            )

            self.define_sanitized_text(new_extracted_page)
            current_chapter.add_page(new_extracted_page)

            ### Now that the chapter has some content assert it's name is
            # the one documented in PageInfo
            if self._is_chapter_beginning_page(page_number):
                self.__assert_chapter_name(page_number, new_extracted_page)

        for chapter in resulting_chapters:
            self.break_chapter_into_paragraphs(chapter)
            for paragraph in chapter.paragraphs:
                self.break_paragraph_into_sentences(paragraph)
        for chapter in resulting_chapters:
            self.reconstitute_paragraphs_spreading_over_two_pages(chapter)
        return resulting_chapters

    def __assert_chapter_name(self, page_number, beginning_page):
        if not self._get_chapter_name(page_number):
            print("The assumption that page number ", page_number)
            print(" starts a chapter was incorrect. ")
            print("Exiting.")
            sys.exit()
        if not "chapter_info" in self.structural_info.pages_info[page_number]:
            print("Chapter page without chapter_info (page number ", page_number, ").")
            print("Exiting")
            sys.exit()
        if not "name" in self.structural_info.pages_info[page_number]["chapter_info"]:
            print(
                "chapter_info of chapter page without name (page number ",
                page_number,
                ").",
            )
            print("Exiting")
            sys.exit()
        chapter_name = self.structural_info.pages_info[page_number]["chapter_info"][
            "name"
        ]
        if not re.search(chapter_name + "[\n\n\n]", beginning_page.text):
            print(
                "Chapter page (page number ",
                page_number,
                ") does not seem to start with ",
                chapter_name,
                ", but with ",
                repr(beginning_page.text),
                sep="",
            )
            print("Exiting.")
            sys.exit()
