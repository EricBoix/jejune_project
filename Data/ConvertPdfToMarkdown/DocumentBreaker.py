import re
from typing import Type

from pypdf import PdfReader

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
        sanitize_page_text_callback,
    ):
        self.document = document
        self.structural_info = structural_info
        self.chapter_splitter = structural_info.get_chapter_splitter()
        self.sanitize_page_text = sanitize_page_text_callback

        # Parse PDF and validate
        self.reader = PdfReader(pdf_filename)
        if len(self.reader.pages) != structural_info.total_page_number:
            WarnAndExit(
                f"Erroneous number of pages: was expecting {structural_info.total_page_number} but got {len(self.reader.pages)}"
            )
        for page_number in range(structural_info.total_page_number):
            self._assert_reader_page_number_is_coherent(page_number)

        # Pre-extract all page texts
        text_extractor = TextExtractor(self.reader, structural_info)
        self.extracted_texts = text_extractor.extract_all()

    def _assert_reader_page_number_is_coherent(self, page_number):
        original_reader_page = self.reader.pages[page_number]
        original_reader_page_number = self.reader.get_page_number(original_reader_page)
        if page_number != original_reader_page_number:
            Warning(
                f"Python page number does not match pypdf::reader page number:\n   - Python page number:  {page_number}\n   - pypdf::reader page number: {original_reader_page_number}"
            )

    def break_document_into_chapters(
        self,
        ExtractedPageDerived: Type = None,
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
            new_extracted_page_layout.set_reference_text(
                f"[Page: {new_extracted_page_layout.reader_page_number} (page number: {new_extracted_page_layout.page_number})]"
            )
            # The usage of ExtractedPage, that can be a derived class, prevents
            # the declaration of this member function to be done in the parent
            # class. This is because although all derived classes will define
            # exactly the same function definition, the concrete ExtractedPage
            # class type might (and thus will) differ from one derivation of
            # a converter to another one.
            new_extracted_page = ExtractedPageDerived(
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
                new_chapter_name = self.chapter_splitter.get_chapter_name(new_extracted_page)
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
            self.sanitize_page_text(new_extracted_page)  # In derived class
            self.structural_info.fix_typos(new_extracted_page)
            current_chapter.add_page(new_extracted_page)
