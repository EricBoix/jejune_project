"""Test that converter output matches reference file."""

from pathlib import Path
from os import path


def test_subchapter_breaking_pattern():
    import re

    # Example taken from
    #  level.name=='Mindfulness is a Lifestyle Change' and
    #  level_content.page_number==45
    SUB_CHAPTER_PATTERN = r"\n\n\n[A-Z| ]{3,50}\n"
    text = "Next, you\nlearn how to keep these already developed insights alive. Finally, you\nfigure out how to develop even deeper levels of insight.\n\n\nMEDITATING ALL THE TIME\nWe must be walking on the Noble Eightfold Path of sīla (moral conduct),\nsamādhi (stability of mind), and paññā (wisdom)."
    match = re.search(SUB_CHAPTER_PATTERN, text)
    assert match is not None
    assert match.start() == 137
    assert match.end() == 164


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
