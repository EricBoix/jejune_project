from ConvertPdfToMarkdown import (
    ConverterBase,
    ExtractedPageBase,
    SuperChapter,
    DocumentWithSubChapters,
)
from Sanitizer import Sanitizer


class Converter(ConverterBase):
    """
    Converter for Zen Flesh, Zen Bones book.
    """

    def __init__(self, pdf_filename, structural_info):
        self.sanitizer = Sanitizer(structural_info)
        document = DocumentWithSubChapters(structural_info.book_title)
        ConverterBase.__init__(self, pdf_filename, document, structural_info)

    def break_document_into_chapters(self):
        return ConverterBase.break_document_into_chapters(
            self, ExtractedPageBase, SuperChapter
        )

    def _page_requires_paragraph_continuation(self, page_number):
        return ConverterBase._page_requires_paragraph_continuation(self, page_number)

    def sanitize_page_text(self, extracted_page):
        self.sanitizer.sanitize_page_text(extracted_page)
