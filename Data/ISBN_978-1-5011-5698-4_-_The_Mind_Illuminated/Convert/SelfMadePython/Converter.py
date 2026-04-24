from ConvertPdfToMarkdown import (
    ConverterBase,
    SuperChapter,
    DocumentWithSubChapters,
)
from Sanitizer import Sanitizer


class Converter(ConverterBase):
    """
    Converter for The Mind Illuminated book.
    """

    def __init__(self, pdf_filename, structural_info):
        self.sanitizer = Sanitizer()
        document = DocumentWithSubChapters(structural_info.book_title)
        ConverterBase.__init__(self, pdf_filename, document, structural_info)

    def break_document_into_chapters(self):
        return ConverterBase.break_document_into_chapters(self, SuperChapter)

    def sanitize_page_text(self, extracted_page):
        self.sanitizer.sanitize_page_text(extracted_page)
