"""Test that converter output matches reference file."""

from pathlib import Path
from os import path


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
