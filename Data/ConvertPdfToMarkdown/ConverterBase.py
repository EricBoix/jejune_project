import re
from typing import Type

from pypdf import PdfReader

from .Model import TopLevelChapter
from .Warning import Warning, WarnAndExit
from .Traces import Debug
from .DocumentBuilder import DocumentBuilder
from .DocumentBreaker import DocumentBreaker


class ConverterBase(DocumentBuilder):
    """
    Class converting the original set of pages extracted from the pypdf::reader
    to a structured document. In order to realize its purpose the Converter
    needs to be manually provided with the structural information (extracted by
    a human reader) that must be promoted to the semantic structure (document,
    chapter, sub-chapter, paragraph...).
    """

    def __init__(self, pdf_filename, document, structural_info):

        # The original pdf document file name that this converter will act from
        self.pdf_filename = pdf_filename

        # Initialize DocumentBuilder
        DocumentBuilder.__init__(self, document, structural_info)

        # Parse the pdf and make some basic coherence checks on the result:
        self.reader = PdfReader(self.pdf_filename)
        if len(self.reader.pages) != self.structural_info.total_page_number:
            WarnAndExit(
                f"Erroneous number of pages: was expecting {self.structural_info.total_page_number} but got {len(self.reader.pages)}"
            )
        for page_number in range(self.structural_info.total_page_number):
            self._assert_reader_page_number_is_coherent(page_number)

        # Eventually realize the conversion
        self.build_document()

    def is_chapter_beginning_page(self, extracted_page):
        # By default we can only assume some structural information, since we
        # don't know whether ExtractedPage will be specialized or not.
        return self.structural_info._is_chapter_beginning_page(
            extracted_page.page_number
        )

    def get_chapter_name(self, extracted_page):
        # By default we can only assume some structural information, since we
        # don't know whether ExtractedPage will be specialized or not.
        return self.structural_info._get_chapter_name(extracted_page.page_number)

    def get_chapter_extracted_page(self, extracted_page):
        """Get the extracted page of the chapter holding the given extracted page."""
        chapter_page_number = self.structural_info._get_chapter_page_number(
            extracted_page.page_number
        )
        chapter_extracted_page = self.document.get_chapter_extracted_page(
            chapter_page_number
        )
        if not chapter_extracted_page:
            WarnAndExit(
                f"Chapter for page number {extracted_page.page_number} not found."
            )
        return chapter_extracted_page

    def breaks_document_into_chapters(
        self,
        ExtractedPageDerived: Type = None,
        ChapterDerived: Type[TopLevelChapter] = None,
    ):
        document_breaker = DocumentBreaker(
            self.reader,
            self.document,
            self.structural_info,
            self.is_chapter_beginning_page,
            self.get_chapter_name,
            self.sanitize_page_text,
            self.fix_typos,
        )
        document_breaker.break_document_into_chapters(
            ExtractedPageDerived, ChapterDerived
        )

    def fix_typos(self, extracted_page):
        """Apply typo fixes on extracted pages that require it."""
        page_number = extracted_page.page_number
        typo_and_fix = self.structural_info.get_typo_and_fix(page_number)
        if typo_and_fix is None:
            return
        typo = typo_and_fix["typo"]
        if not re.search(typo, extracted_page.text):
            Warning(f"Couldn't find typo in extracted page number {page_number}:")
            Warning(f"  - typo: {typo}")
            Warning(f"  - page text: {extracted_page.text}")
            return
        extracted_page.text = re.sub(typo, typo_and_fix["fix"], extracted_page.text)
        Debug(f"Typo fixed on page {page_number}")

    def _assert_reader_page_number_is_coherent(self, page_number):
        # Slightly paranoid check on the reader numbering job coherence.
        original_reader_page = self.reader.pages[page_number]
        original_reader_page_number = self.reader.get_page_number(original_reader_page)
        if page_number != original_reader_page_number:
            Warning(
                f"Python page number does not match pypdf::reader page number:\n   - Python page number:  {page_number}\n   - pypdf::reader page number: {original_reader_page_number}"
            )
        return True

    def get_document(self):
        return self.document
