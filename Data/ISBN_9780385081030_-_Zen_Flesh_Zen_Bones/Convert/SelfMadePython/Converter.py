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

    def is_chapter_beginning_page(self, extracted_page):
        base_says = ConverterBase.is_chapter_beginning_page(self, extracted_page)
        if base_says:
            return True
        return extracted_page.is_chapter_beginning_page()

    def get_chapter_name(self, extracted_page):
        if ConverterBase.is_chapter_beginning_page(self, extracted_page):
            return ConverterBase.get_chapter_name(self, extracted_page)
        # Two stages must be distinguished:
        # - Prior to the construction of the chapter of this page: in this case
        #   the chapter name still stands within the extracted_page content
        #   awaiting to be extracted.
        # - Post construction of the chapter of this page: in which case the
        #   content of the extracted_page no longer contains the name the
        #   chapter. This is because the name of the chapter was extracted
        #   (or removed) from the content of the page and passed to the
        #   constructor of the Chapter object for it to be stored). We must
        #   thus retrieve the name of chapter out of the Chapter object itself.
        chapter_page_number = self.structural_info._get_chapter_page_number(
            extracted_page.page_number
        )
        chapter_name_already_extracted = self.document.get_chapter_name(
            chapter_page_number
        )
        if chapter_name_already_extracted:
            return chapter_name_already_extracted
        # Fold back to the prior to construction case
        return extracted_page.get_chapter_name()
