from os import path
from Converter import Converter
from StructuralInfo import StructuralInfo
from ConvertPdfToMarkdown import (
    print_document_pages,
    print_document_paragraphs,
    print_document_sentences,
)

pdf_filename = path.join(
    path.dirname(__file__),
    "..",
    "..",
    "original_data",
    "2019_-_Sayadaw-U-Tejaniya-Collecting-Gold-Dust-Web-Book-1.pdf",
)

if False:
    print_document_raw_pages(pdf_filename)

converter = Converter(
    pdf_filename=pdf_filename,
    structural_info=StructuralInfo(),
)
document = converter.get_document()
# Generate the markdown file
document.to_markdown("output.md")

# On debugging purposes
if False:
    print_document_pages(document)
    print_document_paragraphs(document)
    print_document_sentences(document)
