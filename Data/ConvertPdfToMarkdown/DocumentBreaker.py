import re
from typing import Type

from pypdf import PdfReader

from .Model import TopLevelChapter
from .PageLayout import PageLayout
from .Warning import WarnAndExit


class DocumentBreaker:
    """
    Breaks a PDF document into chapters by iterating over pages.
    Extracted from ConverterBase to separate PDF-level breaking from text-level
    breaking (handled by LevelBreaker).
    """

    def __init__(
        self,
        reader: PdfReader,
        document,
        structural_info,
        extracted_texts: dict[int, str],
        is_chapter_beginning_page_callback,
        get_chapter_name_callback,
        sanitize_page_text_callback,
        fix_typos_callback,
    ):
        self.reader = reader
        self.document = document
        self.structural_info = structural_info
        self.extracted_texts = extracted_texts
        self.is_chapter_beginning_page = is_chapter_beginning_page_callback
        self.get_chapter_name = get_chapter_name_callback
        self.sanitize_page_text = sanitize_page_text_callback
        self.fix_typos = fix_typos_callback

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

            if not self.is_chapter_beginning_page(new_extracted_page):
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
                new_chapter_name = self.get_chapter_name(new_extracted_page)
                if new_chapter_name is None:
                    WarnAndExit(
                        f"This looks like a new chapter yet it has no name.\nThis was the content of the extracted page: {new_extracted_page}"
                    )

                # Some chapter names include newline characters that must be
                # sanitized in order to create a proper new Chapter object:
                sanitized_new_chapter_name = re.sub("\n", " ", new_chapter_name)
                current_chapter = ChapterDerived(sanitized_new_chapter_name)
                self.document.add_chapter(current_chapter)
                # Yet what we must extract is the "un-sanitized" chapter name
                new_extracted_page.extract_chapter_name(new_chapter_name)

            # We are back to the default flow of treatment
            self.sanitize_page_text(new_extracted_page)  # In derived class
            self.fix_typos(new_extracted_page)
            current_chapter.add_page(new_extracted_page)
