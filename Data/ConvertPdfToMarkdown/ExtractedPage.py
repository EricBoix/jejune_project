class ExtractedPage:
    """
    Representation of a pdf extracted page.

    Attributes
    ----------
    page_number: int
        The index of the page as it appears extracted by pydf::PdfReader()
    original_pdf_page: str
        The text as originally extracted by the constructor caller

    Note: Chapter detection and extraction is handled by chapter_splitter
    classes defined in each book's StructuralInfo.
    """

    def __init__(self, page_number, layout, original_page):
        self.page_number = page_number
        self.page_layout = layout
        self.original_pdf_page = original_page
        self.text = None

    def set_text(self, text_in):
        self.text = text_in

    def __repr__(self):
        return (
            "Extracted paragraph id: " + repr(id(self)) + "\n"
            "Python page number: " + str(self.page_number) + "\n"
            "Reader page number (written on paper and/or as given by pdf viewer): "
            + repr(self.page_layout.reader_page_number)
            + "\n"
            + "Extracted text: "
            + repr(self.text)
        )
