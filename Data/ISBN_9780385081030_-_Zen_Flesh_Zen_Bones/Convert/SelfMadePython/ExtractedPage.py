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
