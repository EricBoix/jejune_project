import re
from ConvertPdfToMarkdown import ConverterBase
from ExtractedPage import ExtractedPage


class Converter(ConverterBase):
    """
    Converter for Collecting Gold Dust book.
    """

    def build_chapters(self):
        return ConverterBase.build_chapters(self, ExtractedPage)

    def _page_requires_paragraph_continuation(self, page_number):
        # if self.structural_info._page_is_illustration(page_number):
        #     return False
        return ConverterBase._page_requires_paragraph_continuation(self, page_number)

    def sanitize_page_text(self, extracted_page):
        # The distributor tag always appears at the bottom of a page
        distributor_regex = self.structural_info.distributor_tag_pattern + "$"
        match = re.search(distributor_regex, extracted_page.text)
        if match:
            extracted_page.text = re.sub(
                self.structural_info.distributor_tag_pattern, "", extracted_page.text
            )

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
