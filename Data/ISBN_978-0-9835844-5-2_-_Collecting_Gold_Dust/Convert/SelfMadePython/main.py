from os import path
from Converter import Converter
from StructuralInfo import StructuralInfo
from pdf_to_markdown import (
    PrintDocument,
    WriteAsLangchainDocuments,
    print_document_raw_pages,
    set_warning_mode,
    set_debug_mode,
)


def main():
    pdf_filename = path.join(
        path.dirname(__file__),
        "..",
        "..",
        "original_data",
        "2019_-_Sayadaw-U-Tejaniya-Collecting-Gold-Dust-Web-Book-1.pdf",
    )

    if False:
        print_document_raw_pages(pdf_filename)

    # set_warning_mode(True)
    # set_debug_mode(True)
    converter = Converter(
        pdf_filename=pdf_filename,
        structural_info=StructuralInfo(),
    )
    document = converter.get_document()
    # Generate the markdown file
    document.to_markdown("output.md")

    # On debugging purposes
    if False:
        PrintDocument(document).pages()
        PrintDocument(document).paragraphs()
        PrintDocument(document).sentences()

    # For downstream Knowledge Graph extraction
    if True:
        WriteAsLangchainDocuments(document).write_sentences(
            "Sentences_as_LangChain_Document.json"
        )


if __name__ == "__main__":
    main()
