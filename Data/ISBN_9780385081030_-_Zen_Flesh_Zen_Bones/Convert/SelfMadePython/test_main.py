"""Test that converter output matches reference file."""

import re
from pathlib import Path


def test_main_output_matches_reference():
    script_dir = Path(__file__).parent

    from Converter import Converter
    from StructuralInfo import StructuralInfo

    # Run conversion (duplicated from main.py)
    converter = Converter(
        pdf_filename=str(
            script_dir
            / ".."
            / ".."
            / "original_data"
            / "1957_-_Paul_Reps_-_Zen_flesh_zen_bones-A_Collection_of_Zen_and_Pre_Zen_Writings_-_Scan_by_OceanofPDF_dot_com.pdf"
        ),
        structural_info=StructuralInfo(),
    )
    document = converter.get_document()
    document.to_markdown(str(script_dir / "output.md"))

    # Compare output.md to reference
    output = (script_dir / "output.md").read_text()
    reference = (
        script_dir
        / ".."
        / ".."
        / "result_data"
        / "1957_-_Paul_Reps_-_Zen_flesh_zen_bones-A_Collection_of_Zen_and_Pre_Zen_Writings_-_Scan_by_OceanofPDF_dot_com_-_local_converter.md"
    ).read_text()
    assert output == reference


class TestChapterRegex:
    """Test the regex pattern for matching chapter headings."""

    CHAPTER_PATTERN = r"([A-Z\d(\n)]+(?<!(\n))(\n){3}(?!(\n))( *){8}OceanofPDF[.]com)"

    def test_fails_on_lowercase_start(self):
        text = "bulls\n\n\n         OceanofPDF.com"
        assert re.search(self.CHAPTER_PATTERN, text) is None

    def test_fails_on_only_two_returns(self):
        text = "BULLS\n\n         OceanofPDF.com"
        assert re.search(self.CHAPTER_PATTERN, text) is None

    def test_fails_on_wrong_ending_string(self):
        text = "BULLS\n\n         OceAnofPDF.com"
        assert re.search(self.CHAPTER_PATTERN, text) is None

    def test_matches_numbered_chapter(self):
        text = "10\nBULLS\n\n\n         OceanofPDF.com"
        match = re.search(self.CHAPTER_PATTERN, text)
        assert match is not None
        assert match.start() == 0

    def test_matches_chapter_title(self):
        text = "THE GATELESS GATE\n\n\n        OceanofPDF.com"
        assert re.search(self.CHAPTER_PATTERN, text) is not None
