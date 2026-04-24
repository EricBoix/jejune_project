import re


class Sanitizer:
    """Sanitizer for Zen Flesh, Zen Bones book."""

    def __init__(self, structural_info):
        # Get distributor pattern from chapter_splitter to avoid duplication
        distributor_name_pattern = (
            structural_info.get_chapter_splitter().distributor_name_pattern
        )
        # The foreword section uses the * (star) character as an enhanced
        # paragraph separator
        self.singularity_enhanced_paragraph_pattern = r"[ ]{45}[*](\n\n)"
        # The distributor tag appears as a footer many (but not all) pages
        self.singularity_distributor_tag_pattern = (
            r"(\n\n)( *)" + distributor_name_pattern
        )
        # Within the '10 BULLS' section, some space was allocated for pictures
        # before the end of the page. This adds an extra set of `\n`
        self.singularity_distributor_tag_pattern_10_bulls_forms = (
            r"(\n){15}" + self.singularity_distributor_tag_pattern
        )

    def sanitize_page_text(self, extracted_page):
        """Remove the distributor name that appears in page footer equivalents."""
        # First remove the rarest sequences
        match = re.search(
            self.singularity_enhanced_paragraph_pattern, extracted_page.text
        )
        if match:
            extracted_page.text = re.sub(
                self.singularity_enhanced_paragraph_pattern, "", extracted_page.text
            )
        # Then clean up the longest sequence
        match = re.search(
            self.singularity_distributor_tag_pattern_10_bulls_forms + "$",
            extracted_page.text,
        )
        if match:
            extracted_page.text = re.sub(
                self.singularity_distributor_tag_pattern_10_bulls_forms,
                "",
                extracted_page.text,
            )
        match = re.search(
            self.singularity_distributor_tag_pattern + "$", extracted_page.text
        )
        if match:
            extracted_page.text = re.sub(
                self.singularity_distributor_tag_pattern, "", extracted_page.text
            )
