"""Test that converter output matches reference file."""

from pathlib import Path
from os import path
import re


class TestChapterRegex:
    """Test the regex patterns for matching subchapter headings."""

    # \u201c is the unicode escape of the LEFT DOUBLE QUOTATION MARK and
    # \u201d is the unicode escape of the RIGHT DOUBLE QUOTATION MARK
    CHAPTER_NAME_CHARACTERS = r"[A-Z|?| \u201c\u201d,]{3,100}"
    MULTI_LINE_CHAPTER_NAME = (
        r"(?:" + CHAPTER_NAME_CHARACTERS + r"\n(?! ))*" + CHAPTER_NAME_CHARACTERS
    )
    # The detection of the end of the heading differs between the top and
    # middle page cases, because for the top page case the subchapter name
    # is not followed by a newline character whereas the middle page is.
    MIDDLE_PAGE_SUBCHAPTER_PATTERN = (
        r"\n\n\n" + MULTI_LINE_CHAPTER_NAME + r"(?=\n[A-Z][a-z]| [A-Z][a-z])"
    )
    TOP_PAGE_SUBCHAPTER_PATTERN = r"^" + MULTI_LINE_CHAPTER_NAME + r"(?= [A-Z][a-z])"

    def test_matches_in_the_middle_of_text(self):
        # Example taken from
        #  level.name=='Mindfulness is a Lifestyle Change' and
        #  level_content.page_number==45
        text = "Next, you\nlearn how to keep these already developed insights alive. Finally, you\nfigure out how to develop even deeper levels of insight.\n\n\nMEDITATING ALL THE TIME\nWe must be walking on the Noble Eightfold Path of sīla (moral conduct),\nsamādhi (stability of mind), and paññā (wisdom)."
        match = re.search(self.MIDDLE_PAGE_SUBCHAPTER_PATTERN, text)
        assert match is not None
        assert match.start() == 137
        assert match.end() == 163

    def test_matches_with_newlines_in_name(self):
        # Example taken from chapter "Mindfulness is a Lifestyle Change" on
        # book page 47.
        text = "The teacher is also inside you.\n\n\n“IF YOU LOOK AFTER THE DHAMMA,\nTHE DHAMMA WILL LOOK AFTER YOU” This work is possible. You need to be patient and work through it for a few years continuously and patiently."
        match = re.search(self.MIDDLE_PAGE_SUBCHAPTER_PATTERN, text)
        assert match is not None
        assert match.start() == 31
        assert match.end() == 96

    def test_fails_for_top_page_when_not_on_top(self):
        # Example taken from chapter "Take a Closer Look" on book page 6.
        text = "Over many years of retreats with my teacher, the late Shwe Oo Min Sayadaw (“Sayadawgyi”), I developed these powers, yet I did not use them in life and did not practice them except on retreat."
        match = re.search(self.TOP_PAGE_SUBCHAPTER_PATTERN, text)
        assert match is None

    def test_matches_for_top_page_when_on_top_page(self):
        # Example taken from chapter "Take a Closer Look" on book page 57.
        text = "RESTLESSNESS You don’t need to try to restrict or rein in a restless mind. Just recognize that if the mind is scattered, that it is scattered."
        match = re.search(self.TOP_PAGE_SUBCHAPTER_PATTERN, text)
        assert match is not None
        assert match.start() == 0
        assert match.end() == 12

    def test_matches_for_top_page_with_commas_and_double_quotes(self):
        # Example taken from chapter "Mindfulness is a Lifestyle Change" on
        # book page 47.
        text = "“IF YOU LOOK AFTER THE DHAMMA, THE DHAMMA WILL LOOK AFTER YOU” This work is possible. You need to be patient and work through it for a few years continuously and patiently."
        match = re.search(self.TOP_PAGE_SUBCHAPTER_PATTERN, text)
        assert match is not None
        assert match.start() == 0
        assert match.end() == 62

    def test_fails_for_top_page_because_no_space_after_multiline_newline(self):
        # Example taken from title page on reader page 4.
        text = "COLLECTING GOLD DUST\n    Nurturing the Dhamma in Daily Living\n\n            Sayadaw U Tejaniya\n\n\n\n       Transcribed by Tony Reardon\n            Edited by Laura Zan"
        match = re.search(self.TOP_PAGE_SUBCHAPTER_PATTERN, text)
        assert match is None


def test_main_output_matches_reference():
    script_dir = Path(__file__).parent

    from Converter import Converter
    from StructuralInfo import StructuralInfo

    pdf_filename = path.join(
        path.dirname(__file__),
        "..",
        "..",
        "original_data",
        "2019_-_Sayadaw-U-Tejaniya-Collecting-Gold-Dust-Web-Book-1.pdf",
    )

    converter = Converter(
        pdf_filename=pdf_filename,
        structural_info=StructuralInfo(),
    )
    document = converter.get_document()
    # Generate the markdown file
    document.to_markdown("output.md")

    # Compare output.md to reference
    output = (script_dir / "output.md").read_text()
    reference = (
        script_dir
        / ".."
        / ".."
        / "result_data"
        / "2019_-_Sayadaw-U-Tejaniya-Collecting-Gold-Dust-Web-Book-1_-_local_converter.md"
    ).read_text()
    assert output == reference
