import os
import sys

sys.path.append(os.path.join("..", "..", "ConvertPdfToMarkdown"))

from Converter import Converter
from Debug import (
    print_document_pages,
    print_document_paragraphs,
    print_document_sentences,
)

converter = Converter(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "..",
        "original_data",
        "2019_-_Sayadaw-U-Tejaniya-Collecting-Gold-Dust-Web-Book-1.pdf",
    )
)
document = converter.get_document()
# Generate the markdown file
document.to_markdown("output.md")

# On debugging purposes
if True:
    print_document_pages(document)
    print_document_paragraphs(document)
    print_document_sentences(document)
