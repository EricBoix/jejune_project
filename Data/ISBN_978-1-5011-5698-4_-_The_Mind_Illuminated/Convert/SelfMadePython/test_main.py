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
            / "2017_-_Culadasa_John_Yates-Matthew_Immergut-Jeremy_Graves_-_The_Mind_Illuminated.pdf"
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
        / "2017_-_Culadasa_John_Yates-Matthew_Immergut-Jeremy_Graves_-_The_Mind_Illuminated_-_local_converter.md"
    ).read_text()
    assert output == reference


class TestChapterRegex:
    """Test the regex pattern for matching chapter headings."""

    CHAPTER_PATTERN = r"([A-Z\d(\n)]+(?<!(\n))(\n){3}(?!(\n))( *){8}OceanofPDF[.]com)"

    SUBCHAPTER_ONE = r"Awakening\n.\n1\nMEDITATION: THE SCIENCE AND ART OF LIVING\nMeditation is a science"
    SUBCHAPTER_TWO = r"tgo.\nA MODERN ROAD MAP FOR MEDITATION\nThis book is the"
    SUBCHAPTER_THREE = r"the book.\nPUTTING THIS PRACTICE INTO CONTEXT\nThe meditation"

    def test_fails_on_lowercase_start(self):
        text = "bulls\n\n\n         OceanofPDF.com"
        assert re.search(self.CHAPTER_PATTERN, text) is None
