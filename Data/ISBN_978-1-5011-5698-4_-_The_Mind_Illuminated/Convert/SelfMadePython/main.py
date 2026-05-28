from os import path
from Converter import Converter
from StructuralInfo import StructuralInfo
from pdf_to_markdown import (
    print_document_raw_pages,
    set_warning_mode,
    PrintDocument,
)
from markdown_pdf import MarkdownPdf, Section

pdf_filename = path.join(
    path.dirname(__file__),
    "..",
    "..",
    "original_data",
    "2017_-_Culadasa_John_Yates-Matthew_Immergut-Jeremy_Graves_-_The_Mind_Illuminated.pdf",
)

if False:
    print_document_raw_pages(pdf_filename)

set_warning_mode(True)
converter = Converter(
    pdf_filename=pdf_filename,
    structural_info=StructuralInfo(),
)

document = converter.get_document()

# Generate the markdown file
target_file_basename = "output"
document.to_markdown(target_file_basename + ".md")

# Generate the pdf file out of markdown content
pdf = MarkdownPdf(toc_level=4, optimize=True)
pdf.add_section(Section(open("output.md", encoding="utf-8").read()))
pdf.meta["title"] = "Pdf generated out of markdown"
pdf.save(target_file_basename + ".pdf")

# On debugging purposes
if False:
    printer = PrintDocument(document)
    # printer.pages()
    # printer.paragraphs()
    printer.with_subchapter_sentences()
