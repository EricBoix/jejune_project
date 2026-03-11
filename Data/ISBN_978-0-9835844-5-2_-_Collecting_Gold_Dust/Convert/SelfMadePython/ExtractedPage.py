import sys
import re
from ConvertPdfToMarkdown import ExtractedPageBase


class ExtractedPage(ExtractedPageBase):

    def __init__(self, page_number, layout, original_page):
        ExtractedPageBase.__init__(self, page_number, layout, original_page)
        # The following regex stands for
        # (?<!(\n)): negative lookbehind for a newline (that is: make sure
        #            we start the match at the first newline occurrence)
        # (\n){6}: match six newlines (note: but they can be more than that
        #          standing afterwards. Hence, if we where to leave the regex
        #          like that, it could be that they are more newlines than 6.)
        # (?!(\n)): look-forward stating that when matching the above 6 newlines
        #          the next character can NOT be a newline.
        # The whole regex thus states: match EXACTLY (no more, no less) 6
        # newlines.
        self.chapter_name_separator_regex = r"(?<!(\n))(\n){6}(?!(\n))"
        self.chapter_name_separator_first_occurrence = 100
        self.removed_header = None

        original_page_text = self.original_pdf_page.extract_text(
            extraction_mode="layout"
        )

        # Remove the heading bunch of whitespaces (and assimilated characters)
        self.text = original_page_text.lstrip()

    def set_removed_header(self, removed_header):
        self.removed_header = removed_header

    def __repr__(self):
        result = ExtractedPageBase.__repr__(self) + "\n"
        if self.removed_header is not None:
            result += "Removed header: " + repr(self.removed_header)
        return result

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
