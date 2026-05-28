from os import path
from Converter import Converter
from StructuralInfo import StructuralInfo
from pdf_to_markdown import (
    PrintDocument,
    print_document_raw_pages,
    set_warning_mode,
    set_debug_mode,
)

pdf_filename = path.join(
    path.dirname(__file__),
    "..",
    "..",
    "original_data",
    "1957_-_Paul_Reps_-_Zen_flesh_zen_bones-A_Collection_of_Zen_and_Pre_Zen_Writings_-_Scan_by_OceanofPDF_dot_com.pdf",
)

if False:
    print_document_raw_pages(pdf_filename)

set_warning_mode(True)
set_debug_mode(True)
converter = Converter(
    pdf_filename=pdf_filename,
    structural_info=StructuralInfo(),
)
document = converter.get_document()
# Generate the markdown file
document.to_markdown("output.md")

# On debugging purposes
if True:
    printer = PrintDocument(document)
    # printer.pages()
    # printer.paragraphs()
    printer.with_subchapter_sentences()
