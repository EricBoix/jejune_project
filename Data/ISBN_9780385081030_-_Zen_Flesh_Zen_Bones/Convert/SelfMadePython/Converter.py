from ConvertPdfToMarkdown import (
    ConverterBase,
    SuperChapter,
    DocumentWithSubChapters,
)
from ExtractedPage import ExtractedPage


class Converter(ConverterBase):
    """
    Converter for Zen Flesh, Zen Bones book.
    """

    def __init__(self, pdf_filename, structural_info):
        document = DocumentWithSubChapters(structural_info.book_title)
        ConverterBase.__init__(self, pdf_filename, document, structural_info)

    def breaks_document_into_chapters(self):
        return ConverterBase.breaks_document_into_chapters(
            self, ExtractedPage, SuperChapter
        )

    def _page_requires_paragraph_continuation(self, page_number):
        return ConverterBase._page_requires_paragraph_continuation(self, page_number)

    def sanitize_page_text(self, extracted_page):
        extracted_page.sanitize_footer()
