from pdf_to_markdown import (
    ConverterBase,
    SuperChapter,
    DocumentWithSubChapters,
)


class Converter(ConverterBase):
    """
    Converter for Zen Flesh, Zen Bones book.
    """

    def __init__(self, pdf_filename, structural_info):
        document = DocumentWithSubChapters(structural_info.book_title)
        ConverterBase.__init__(self, pdf_filename, document, structural_info)

    def break_document_into_chapters(self):
        return ConverterBase.break_document_into_chapters(self, SuperChapter)
