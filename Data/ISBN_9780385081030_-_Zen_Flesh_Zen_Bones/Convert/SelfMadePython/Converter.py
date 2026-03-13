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
