import sys
import re

from ConvertPdfToMarkdown import ConverterBase
from ExtractedPage import ExtractedPage


class Converter(ConverterBase):
    """
    Converter for The Mind Illuminated book.
    """

    def build_chapters(self):
        return ConverterBase.build_chapters(self, ExtractedPage)

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
        extracted_page.sanitize_figures()

    def __assert_chapter_name(self, page_number, beginning_page):
        chapter_name = self.structural_info._get_chapter_name(page_number)
        if not re.search(chapter_name + "[\n\n\n]", beginning_page.sentence):
            print(
                "Chapter page (page number ",
                page_number,
                ") does not seem to start with ",
                chapter_name,
                ", but with ",
                repr(beginning_page.sentence),
                sep="",
            )
            print("Exiting.")
            sys.exit()

    def assert_chapters_name_coherence(self):
        for chapter in self.document.get_chapters():
            first_page_number = chapter.pages[0].page_number
            first_sentence = chapter.get_paragraph(0).get_sentence(0)
            self.__assert_chapter_name(first_page_number, first_sentence)
