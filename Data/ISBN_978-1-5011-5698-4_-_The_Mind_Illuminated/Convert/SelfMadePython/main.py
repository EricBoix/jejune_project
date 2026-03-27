import os
from markdown_pdf import MarkdownPdf, Section
from Converter import Converter
from StructuralInfo import StructuralInfo
from ConvertPdfToMarkdown import PrintDocument

converter = Converter(
    pdf_filename=os.path.join(
        os.path.dirname(__file__),
        "..",
        "..",
        "original_data",
        "2017_-_Culadasa_John_Yates-Matthew_Immergut-Jeremy_Graves_-_The_Mind_Illuminated.pdf",
    ),
    structural_info=StructuralInfo(),
)
# FIXME converter.assert_chapters_name_coherence()
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
    PrintDocument(document).pages()
    PrintDocument(document).paragraphs()
    PrintDocument(document).sentences()
