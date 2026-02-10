class ExtractedPage:
    """
    Representation of a pdf extracted page
    Attributes
    ----------
    page_number: int
        The index of the page as it appears extracted by pydf::PdfReader()
    original_pdf_page: str
        the text as original extracted by the constructor caller
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
            + "Original Text: "
            + repr(self.original_pdf_page.extract_text(extraction_mode="layout"))
            + "\n"
            + "Extracted text: "
            + repr(self.text)
        )
