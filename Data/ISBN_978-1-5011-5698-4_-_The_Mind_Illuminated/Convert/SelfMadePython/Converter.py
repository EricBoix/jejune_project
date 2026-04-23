from ConvertPdfToMarkdown import (
    ConverterBase,
    SuperChapter,
    DocumentWithSubChapters,
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
