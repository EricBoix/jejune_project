import sys
import re
from ConvertPdfToMarkdown import ExtractedPageBase


class ExtractedPage(ExtractedPageBase):

    def __init__(self, page_number, layout, original_page):
        ExtractedPageBase.__init__(self, page_number, layout, original_page)

        ######## Regex (pattern) related section
        ### PDF distributor tag (a specific string)
        self.distributor_name_pattern = r"OceanofPDF[.]com"

        ######### Chapter related
        # Three whitespaces (more or less)
        self.chapter_name_extractor_regex = r"(\n){3}"
        # The pattern that should match a chapter title definition
        self.chapter_name_separator_regex = (
            # a bunch of capital letters, or digits with possible white spaces
            #  and/or returns
            r"[A-Z\d (\n)]+"
            # _exactly_ three returns,
            + r"(?<!(\n))"
            + self.chapter_name_extractor_regex
            + r"(?!(\n))"
            # at least 8 white spaces,
            + r"( *){8}"
            # a specific string (refer above)
            + self.distributor_name_pattern
        )
        # The maximum number of characters within an extracted page to look
        # for a chapter title:
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
        chapter_name = re.split(self.chapter_name_extractor_regex, self.text)
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

    def sanitize_footer():
        """Remove the distributor name that appears in page footer equivalents (the last string of a page)"""
        return

    def extract_chapter_name(self, chapter_name):
        if re.search(self.distributor_name_pattern, self.text) is None:
            # The chapter name was not extracted through a pattern. Fold to
            # the default method:
            ExtractedPageBase.extract_chapter_name(self, chapter_name)
            return
        # We are in the case where the name of the chapter was extracted with
        # a pattern matching rule and that it already matches (because
        # of the logic of the caller that is in the process of creating the
        # encountered new chapter):
        self.text = re.sub(self.chapter_name_separator_regex, "", self.text)
