"""Test that converter output matches reference file."""

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
