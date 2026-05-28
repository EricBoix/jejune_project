import sys
import roman

from pdf_to_markdown import (
    ConverterBase,
    SuperChapter,
    DocumentWithSubChapters,
    WarnAndExit,
)


class Converter(ConverterBase):
    """
    Converter for Collecting Gold Dust book.
    """

    def __init__(self, pdf_filename, structural_info):
        structural_info.set_page_header_callback(self.get_page_header)
        document = DocumentWithSubChapters(structural_info.book_title)
        ConverterBase.__init__(self, pdf_filename, document, structural_info)

    def break_document_into_chapters(self):
        return ConverterBase.break_document_into_chapters(self, SuperChapter)

    def _page_requires_paragraph_continuation(self, page_number):
        if self.structural_info._page_is_illustration(page_number):
            return False
        return ConverterBase._page_requires_paragraph_continuation(self, page_number)

    def _chapter_splitter(self):
        return self.structural_info.get_chapter_splitter()

    def get_chapter_name(self, extracted_page):
        # Two stages must be distinguished:
        # - Prior to the construction of the chapter of this page: in this case
        #   the chapter name still stands within the extracted_page content
        #   awaiting to be extracted.
        # - Post construction of the chapter of this page: in which case the
        #   content of the extracted_page no longer contains the name the
        #   chapter. This is because the name of the chapter was extracted
        #   (or removed) from the content of the page and passed to the
        #   constructor of the Chapter object for it to be stored). We must
        #   thus retrieve the name of chapter out of the Chapter object itself.
        chapter_page_number = self.structural_info._get_chapter_page_number(
            extracted_page.page_number
        )
        chapter_name_already_extracted = self.document.get_chapter_name(
            chapter_page_number
        )
        if chapter_name_already_extracted:
            return chapter_name_already_extracted
        # Fold back to the prior to construction case (use chapter_splitter)
        return self._chapter_splitter().get_chapter_name(extracted_page)

    def chapter_page_header(self, extracted_page):
        return (
            self.get_chapter_name(extracted_page)
            + r" \| "
            + self.structural_info.convert_to_logical_page_number(
                extracted_page.page_number
            )
        )

    def get_page_header(self, extracted_page):
        page_number = extracted_page.page_number
        if page_number < 0 or page_number > self.structural_info.total_page_number:
            print("Page number is outside of book page numeration.")
            print("Exiting")
            sys.exit()

        # Pages explicitly flagged as headless, well, are headless:
        if self.structural_info._page_is_headless(page_number):
            return ""

        # First headers of pages starting a new chapter have that new
        # chapter name as header
        if self._chapter_splitter().holds_new_chapter(extracted_page):
            return self.get_chapter_name(extracted_page)

        ####### Concerning the Preamble (from page 0 to 20 included)
        # Before the body of the book, there is a (quite lengthy) preamble that
        # has quite specific header rules :
        if page_number < 10:
            # Default value for a preamble header is to be empty
            return ""
        if page_number >= 10 and page_number < 15:
            return roman.toRoman(page_number).lower()
        if page_number == 16:
            # The following hardcoded value for page 16 is because that page
            # doesn't follow the above logical rule. The following fix for page
            # 16 _is_ correct ! It is the pdf that is erroneous.
            return roman.toRoman(16).lower() + roman.toRoman(16).lower()
        if page_number == 17:
            return ""
        if page_number >= 18 and page_number < 20:
            return self.structural_info.convert_to_logical_page_number(page_number)
        if page_number <= 19 and page_number <= 21:
            return ""

        ####### Concerning the body of the book.
        # Pages of the body of the book, have a headers that follow a simple
        # constructive rule with some exceptions...

        if (page_number % 2) == 0:
            # Odd pages have a header that is simply the book title followed
            # by their page number
            return self.structural_info.book_title_page_header(page_number)
        if (page_number % 2) != 0:
            if page_number == 133:
                # Page 133 has a brain damaged header that doesn't
                # follow the even page header rule (although it is a near
                # miss). The only possible fix is to define an exception:
                fake_extracted_page = type("", (), {})()
                fake_extracted_page.page_number = 133
                logical_page_number = (
                    self.structural_info.convert_to_logical_page_number(133)
                )
                return (
                    self.structural_info.book_title
                    + self.get_chapter_name(fake_extracted_page)
                    + " ||"
                    + logical_page_number
                    + logical_page_number
                )
            else:
                # Even pages have a different header pattern based on the current
                # chapter name
                return self.chapter_page_header(extracted_page)

        WarnAndExit("Header for page number ", page_number, " is not defined")
