import sys
import re
from ConvertPdfToMarkdown import ExtractedPageBase


class ExtractedPage(ExtractedPageBase):

    def __init__(self, page_number, layout, original_page):
        ExtractedPageBase.__init__(self, page_number, layout, original_page)

        ######## Regex (pattern) related section
        ### PDF distributor tag (a specific string)
        self.distributor_name_pattern = r"OceanofPDF[.]com"

        #### Used for removal (when it appears outside of titles)
        # The foreword section uses the * (star) character as an enhanced
        # paragraph separator
        self.singularity_enhanced_paragraph_pattern = r"[ ]{45}[*](\n\n)"
        # The distributor tag appears as a footer many (but not all) pages
        self.singularity_distributor_tag_pattern = (
            r"(\n\n)( *)" + self.distributor_name_pattern
        )
        # Within the '10 BULLS' section, some space was allocated for pictures
        # before the end of the page. This adds an extra set of `\n`
        self.singularity_distributor_tag_pattern_10_bulls_forms = (
            r"(\n){15}" + self.singularity_distributor_tag_pattern
        )

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

    def sanitize_footer(self):
        """Remove the distributor name that appears in page footer equivalents (the last string of a page)"""
        # First remove the rarest sequences
        match = re.search(self.singularity_enhanced_paragraph_pattern, self.text)
        if match:
            self.text = re.sub(
                self.singularity_enhanced_paragraph_pattern, "", self.text
            )
        # Then clean up the longest sequence
        match = re.search(
            self.singularity_distributor_tag_pattern_10_bulls_forms + "$", self.text
        )
        if match:
            self.text = re.sub(
                self.singularity_distributor_tag_pattern_10_bulls_forms, "", self.text
            )
        match = re.search(self.singularity_distributor_tag_pattern + "$", self.text)
        if match:
            self.text = re.sub(self.singularity_distributor_tag_pattern, "", self.text)

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
