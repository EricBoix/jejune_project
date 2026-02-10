from Model import Document
from Converter import Converter
from Debug import (
    print_document_pages,
    print_document_paragraphs,
    print_document_sentences,
)

converter = Converter()
document = converter.get_document()
# Generate the markdown file
document.to_markdown("output.md")

# On debugging purposes
if True:
    print_document_pages(document)
    print_document_paragraphs(document)
    print_document_sentences(document)
