import sys
import re
import os

sys.path.append(os.path.join("..", "..", "..", "ConvertPdfToMarkdown"))
from ConverterBase import ConverterBase
from PageLayout import PageLayout
from Model import Chapter
from ExtractedPageBase import ExtractedPageBase as ExtractedPage


class Converter(ConverterBase):
    """
    Converter for The Mind Illuminated book.
    """

    def build_chapters(self):
        resulting_chapters = []
        current_chapter = None
        for page_number in range(0, self.structural_info.total_page_number):

            if self.structural_info._page_is_dropped(page_number):
                continue

            if self.structural_info._is_chapter_beginning_page(page_number):
                new_chapter_name = self.structural_info._get_chapter_name(page_number)
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
                self.structural_info.convert_to_logical_page_number(page_number),
                page_number,
            )
            new_extracted_page_layout.set_reference_text(
                "[Page: "
                + str(new_extracted_page_layout.reader_page_number)
                + " (page number: "
                + str(new_extracted_page_layout.page_number)
                + ")]"
            )
            # The usage of ExtractedPage, that can be a derived class, prevents
            # the declaration of this member function to be done in the parent
            # class. This is because although all derived classes with define
            # exactly the same function definition, the concrete ExtractedPage
            # class type might (and thus will) differ from one derivation of
            # a converter to another one.
            new_extracted_page = ExtractedPage(
                page_number,
                new_extracted_page_layout,
                self.reader.pages[page_number],  # Original page
            )

            self.sanitized_page_text(new_extracted_page)
            current_chapter.add_page(new_extracted_page)

        for chapter in resulting_chapters:
            self.break_chapter_into_paragraphs(chapter)
            for paragraph in chapter.paragraphs:
                self.break_paragraph_into_sentences(paragraph)
        for chapter in resulting_chapters:
            self.reconstitute_paragraphs_spreading_over_two_pages(chapter)
        return resulting_chapters

    def sanitized_page_text(self, extracted_page):
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

    def __assert_chapter_name(self, page_number, beginning_page):
        chapter_name = self.structural_info._get_chapter_name(page_number)
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

    def assert_chapters_name_coherence(self):
        for chapter in self.document.get_chapters():
            first_page_number = chapter.pages[0].page_number
            first_sentence = chapter.get_paragraph(0).get_sentence(0)
            self.__assert_chapter_name(first_page_number, first_sentence)
