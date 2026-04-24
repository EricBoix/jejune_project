import re
from abc import ABC, abstractmethod
from .Warning import Warning, WarnAndExit
from .Traces import Debug


class StructuralInfoBase(ABC):
    """
    Base class for structural information about a PDF document.

    Subclasses must implement pages_info property returning a dict:
    {
        0: {                                # page number as key
            "type": "chapter",              # "chapter" or "generic"
            "chapter_info": {               # required for "chapter" type
                "name": "Preamble",
                "illumination_delimiter": None,
            },
        },
        1: {
            "type": "generic",
            "drop_page": True,              # optional flag to drop content
        },
    }
    """

    # Dictionary key constants
    KEY_TYPE = "type"
    KEY_CHAPTER_INFO = "chapter_info"
    KEY_NAME = "name"
    KEY_DROP_PAGE = "drop_page"
    KEY_TYPO_AND_FIX = "typo_and_fix"
    KEY_TYPO = "typo"
    KEY_FIX = "fix"

    @property
    @abstractmethod
    def pages_info(self) -> dict:
        """Return dict mapping page numbers to their structural info."""
        ...

    @property
    @abstractmethod
    def total_page_number(self) -> int:
        """Return total number of pages in the PDF document."""
        ...

    def __init__(self):
        # Technical (optimisation) variable used to hold the correspondance
        # between a given page number and the chapter to which that page
        # belongs to. In other terms, within this dictionary
        #  - a key is a page number
        #  - the associated value holds the current chapter number for that key
        self._chapter_page = {}
        self._chapter_splitter_instance = None

    def get_chapter_splitter(self):
        """Get or create the chapter splitter for this document.

        Each derived StructuralInfo defines a chapter_splitter inner class.
        """
        if self._chapter_splitter_instance is None:
            self._chapter_splitter_instance = self.chapter_splitter(self)
        return self._chapter_splitter_instance

    def set_chapter_page_number(self, page_number: int, chapter_page_number: int):
        """Set the chapter page number of the page designated by page number.

        :param int page_number: The page number of the page for which we are setting the chapter (page)
        :param int chapter_page_number The page number of the chapter (beginning) to which the designated belongs to.
        """
        if page_number in self._chapter_page:
            WarnAndExit(
                f"Trying to overwrite chapter page of page number {page_number}."
            )
        self._chapter_page[page_number] = chapter_page_number

    def _page_is_dropped(self, page_number):
        if not page_number in self.pages_info:
            return False
        if not self.KEY_DROP_PAGE in self.pages_info[page_number]:
            return False
        return True

    def _page_is_skipped(self, page_number):
        """
        The derived classes might overload this definition with their specific considerations.
        """
        return self._page_is_dropped(page_number)

    def _get_chapter_page_number(self, page_number):
        if page_number not in self._chapter_page:
            WarnAndExit(f"Unknown chapter page of page number {page_number}.")
        return self._chapter_page[page_number]

    def _get_chapter_page(self, page_number):
        chapter_page_number = self._get_chapter_page_number(page_number)
        return self.pages_info[chapter_page_number]

    def _get_chapter_info(self, page_number):
        chapter_page = self._get_chapter_page(page_number)
        return chapter_page[self.KEY_CHAPTER_INFO]

    def _get_chapter_name(self, page_number):
        chapter_info = self._get_chapter_info(page_number)
        return chapter_info.get(self.KEY_NAME)

    def _holds_new_chapter(self, page_number):
        if not page_number in self.pages_info:
            return False
        if not self.KEY_TYPE in self.pages_info[page_number]:
            return False
        if self.pages_info[page_number][self.KEY_TYPE] == "chapter":
            return True
        return False

    def get_typo_and_fix(self, page_number):
        if not page_number in self.pages_info:
            return None
        if not self.KEY_TYPO_AND_FIX in self.pages_info[page_number]:
            return None
        return self.pages_info[page_number][self.KEY_TYPO_AND_FIX]

    def fix_typos(self, extracted_page):
        """Apply typo fixes on extracted pages that require it."""
        page_number = extracted_page.page_number
        typo_and_fix = self.get_typo_and_fix(page_number)
        if typo_and_fix is None:
            return
        typo = typo_and_fix[self.KEY_TYPO]
        if not re.search(typo, extracted_page.text):
            Warning(f"Couldn't find typo in extracted page number {page_number}:")
            Warning(f"  - typo: {typo}")
            Warning(f"  - page text: {extracted_page.text}")
            return
        extracted_page.text = re.sub(typo, typo_and_fix[self.KEY_FIX], extracted_page.text)
        Debug(f"Typo fixed on page {page_number}")

    def _get_page_number_finishing_last_paragraph(self, page_number):
        """
        A page that is followed by one (or many) skipped pages will need to skip such pages in order to retrieve the end of its last paragraph.
        Return the page number of the first page that holds the content of the end of the paragraph.
        """
        next_page_number = page_number + 1
        while self._page_is_skipped(next_page_number):
            next_page_number += 1
        return next_page_number

    def convert_to_logical_page_number(self, page_number):
        """
        Some pdf books (generally also available in paper form) propose an
        ad-hoc page numbering scheme (think e.g. of roman numbering based page numbers or starting the numbering after the pages holding the editor's
        notes). There is thus a correspondance between the page number at the
        pdf language level (that always exists) and the optional editor's page numbering.
        Parameters
        ----------
        page_number : int
            the page number at the PDF level
        Returns
        -------
        the page number (as string) as printed on the page (editor's choice)
        """
        return str(page_number)

    def sanitize_page_text(self, extracted_page):
        """Sanitize page text. Override in derived classes for book-specific sanitization."""
        pass
