import re
from ConvertPdfToMarkdown import (
    ConverterBase,
    SuperChapter,
    DocumentWithSubChapters,
    WarnAndExit,
)
from ExtractedPage import ExtractedPage


class Converter(ConverterBase):
    """
    Converter for The Mind Illuminated book.
    """

    def __init__(self, pdf_filename, structural_info):
        document = DocumentWithSubChapters(structural_info.book_title)
        ConverterBase.__init__(self, pdf_filename, document, structural_info)

    def breaks_document_into_chapters(self):
        return ConverterBase.breaks_document_into_chapters(
            self, ExtractedPage, SuperChapter
        )

    def sanitize_page_text(self, extracted_page):
        """
        After extraction of the text from the original pdf, some ad hoc
        manual cleaning is alas required.
        """
        extracted_page.sanitize_figures()

    def __assert_chapter_name(self, page_number, beginning_page):
        chapter_name = self.structural_info._get_chapter_name(page_number)
        if not re.search(chapter_name + "[\n\n\n]", beginning_page.text):
            WarnAndExit(
                f"Chapter page (page number {page_number}) does not seem to start with {chapter_name}, but with {repr(beginning_page.text)}"
            )

    def assert_chapters_name_coherence(self):
        for chapter in self.document.get_chapters():
            first_page_number = chapter.pages[0].page_number
            first_sentence = chapter.get_paragraph(0).get_sublevel(0)
            self.__assert_chapter_name(first_page_number, first_sentence)

    def is_chapter_beginning_page(self, extracted_page):
        return extracted_page.is_chapter_beginning_page()

    def get_chapter_name(self, extracted_page):
        return extracted_page.get_chapter_name()
