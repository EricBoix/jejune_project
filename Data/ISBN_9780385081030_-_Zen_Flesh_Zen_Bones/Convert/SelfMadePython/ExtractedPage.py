import sys
import re
from ConvertPdfToMarkdown import ExtractedPageBase


class ExtractedPage(ExtractedPageBase):

    def __init__(self, page_number, layout, original_page):
        ExtractedPageBase.__init__(self, page_number, layout, original_page)
        # FIXME : remove the two following members (that do not belong here
        # since they wer copied from a different book) and watch things
        # break down !
        self.chapter_name_separator_regex = r"(?<!(\n))(\n){6}(?!(\n))"
        self.chapter_name_separator_first_occurrence = 100

        original_page_text = self.original_pdf_page.extract_text(
            extraction_mode="layout"
        )

        # Remove the heading bunch of whitespaces (and assimilated characters)
        self.text = original_page_text.lstrip()

    def is_chapter_beginning_page(self):
        match = re.search(self.chapter_name_separator_regex, self.text)
        if not match:
            return False
        if match.start() > self.chapter_name_separator_first_occurrence:
            # The separator has to be encountered quite early in the page.
            # This is quite artificial and done to weed out odd occurrences...
            return False
        return True

    def get_chapter_name(self):
        chapter_name = re.split(self.chapter_name_separator_regex, self.text)
        if not chapter_name:
            print(
                "Chapter name ",
                chapter_name,
                " not found in extracted page ",
                self.text,
            )
            print("Exiting")
            sys.exit()
        return chapter_name[0]
