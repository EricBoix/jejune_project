import os
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
        "2017_-_Culadasa_John_Yates-Matthew_Immergut-Jeremy_Graves_-_The_Mind_Illuminated.pdf",
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
