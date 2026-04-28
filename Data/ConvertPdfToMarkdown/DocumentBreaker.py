import re
from typing import Type

from pypdf import PdfReader

from .ExtractedPage import ExtractedPage
from .Model import TopLevelChapter
from .PageLayout import PageLayout
from .TextExtractor import TextExtractor
from .Warning import Warning, WarnAndExit


class DocumentBreaker:
    """
    Breaks a PDF document into chapters by iterating over pages.
    Handles PDF reading, text extraction, and chapter breaking.
    """

    def __init__(
        self,
        pdf_filename,
        document,
        structural_info,
    ):
        self.document = document
        self.structural_info = structural_info
        self.chapter_splitter = structural_info.get_chapter_splitter()

        # Parse PDF and validate
        self.reader = PdfReader(pdf_filename)
        self._validate_all_pages()

        # Pre-extract all page texts
        text_extractor = TextExtractor(self.reader, structural_info)
        self.extracted_texts = text_extractor.extract_all()

    def _validate_all_pages(self):
        """Perform all upfront page validation."""
        if len(self.reader.pages) != self.structural_info.total_page_number:
            WarnAndExit(
                f"Erroneous number of pages: was expecting "
                f"{self.structural_info.total_page_number} but got {len(self.reader.pages)}"
            )
        for page_number in range(self.structural_info.total_page_number):
            self._validate_page(page_number)

    def _validate_page(self, page_number):
        """Validate a single page."""
        self._validate_reader_page_coherence(page_number)
        self._validate_page_structure(page_number)

    def _validate_reader_page_coherence(self, page_number):
        """Validate reader page number matches expected."""
        original_reader_page = self.reader.pages[page_number]
        original_reader_page_number = self.reader.get_page_number(original_reader_page)
        if page_number != original_reader_page_number:
            Warning(
                f"Python page number does not match pypdf::reader page number:\n"
                f"   - Python page number:  {page_number}\n"
                f"   - pypdf::reader page number: {original_reader_page_number}"
            )

    def _validate_page_structure(self, page_number):
        """Validate page has required structural info."""
        pages_info = self.structural_info.pages_info
        if page_number not in pages_info:
            return

        page_info = pages_info[page_number]
        key_type = self.structural_info.KEY_TYPE
        key_chapter_info = self.structural_info.KEY_CHAPTER_INFO
        key_name = self.structural_info.KEY_NAME

        if page_info.get(key_type) == "chapter":
            if key_chapter_info not in page_info:
                WarnAndExit(f"Chapter page {page_number} missing chapter_info.")
            elif key_name not in page_info[key_chapter_info]:
                WarnAndExit(f"Chapter page {page_number} missing name in chapter_info.")

    def break_document_into_chapters(
        self,
        ChapterDerived: Type[TopLevelChapter] = None,
    ):
        current_chapter = None
        for page_number in range(0, self.structural_info.total_page_number):

            if self.structural_info._page_is_dropped(page_number):
                continue

            ### Create a new extracted page:
            new_extracted_page_layout = PageLayout(
                self.structural_info.convert_to_logical_page_number(page_number),
                page_number,
            )
            new_extracted_page = ExtractedPage(
                page_number,
                new_extracted_page_layout,
                self.reader.pages[page_number],  # Original page
            )
            new_extracted_page.set_text(self.extracted_texts[page_number])

            if not self.chapter_splitter.holds_new_chapter(new_extracted_page):
                # When the new extracted page is not the beginning of a chapter
                # we must still assert that the current_chapter was previously
                # encountered
                if not current_chapter:
                    # We didn't encounter a first chapter yet the first
                    # encountered page is not a page starting a chapter.
                    # Something went really wrong.
                    WarnAndExit(
                        f"Any chapter must start with...a chapter typed page.\nNote: we didn't encounter the first chapter yet.\nThis was the content of the extracted page: {new_extracted_page}"
                    )
                self.structural_info.set_chapter_page_number(
                    new_extracted_page.page_number,
                    current_chapter.page_layout.page_number,
                )
            else:
                # This new extracted page is the one of a new chapter. We must
                # thus create it (a Chapter object) as such and define this new
                # Chapter as the current_chapter:
                self.structural_info.set_chapter_page_number(
                    new_extracted_page.page_number,
                    new_extracted_page.page_number,
                )
                new_chapter_name = self.chapter_splitter.get_chapter_name(
                    new_extracted_page
                )
                if new_chapter_name is None:
                    WarnAndExit(
                        f"This looks like a new chapter yet it has no name.\nThis was the content of the extracted page: {new_extracted_page}"
                    )

                # Some chapter names include newline characters that must be
                # sanitized in order to create a proper new Chapter object:
                sanitized_new_chapter_name = re.sub("\n", " ", new_chapter_name)
                current_chapter = ChapterDerived(sanitized_new_chapter_name)
                self.document.add_chapter(current_chapter)
                # Remove chapter name from page text
                self.chapter_splitter.extract_chapter_name(
                    new_extracted_page, new_chapter_name
                )

            # We are back to the default flow of treatment
            self.structural_info.sanitize_page_text(new_extracted_page)
            self.structural_info.fix_typos(new_extracted_page)
            current_chapter.add_page(new_extracted_page)
