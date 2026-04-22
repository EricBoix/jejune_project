import re
from abc import ABC
from .Warning import Warning, WarnAndExit


class ExtractedPageBase(ABC):
    """
    Representation of a pdf extracted page.

    Attributes
    ----------
    page_number: int
        The index of the page as it appears extracted by pydf::PdfReader()
    original_pdf_page: str
        The text as originally extracted by the constructor caller

    Subclasses should override:
    - is_chapter_beginning_page(): Returns True if page starts a chapter
    - extract_chapter_name(): Extracts chapter name from page text (optional)
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

    def is_chapter_beginning_page(self):
        """Sometimes (is a derived class) a rule applied on the text of the
        the extracted page suffice to decide whether the extracted page is
        the beginning of a chapter or not"""
        return False

    def extract_chapter_name(self, chapter_name):
        if not re.search(chapter_name, self.text):
            Warning(
                f"chapter name {chapter_name} was not found in extracted page {self.text}"
            )
            return
        chapter_text = self.text.lstrip(chapter_name)
        if not chapter_text:
            WarnAndExit(
                f"Chapter name extraction yields an empty text.\nWas trying to extract chapter name: {chapter_name} Out of ExtractedPageBase text: {self.text}"
            )
        self.text = chapter_text
