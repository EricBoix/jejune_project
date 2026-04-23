import sys
import re
import roman

from ConvertPdfToMarkdown import (
    ConverterBase,
    SuperChapter,
    DocumentWithSubChapters,
    WarnAndExit,
)
from ExtractedPage import ExtractedPage


class Converter(ConverterBase):
    """
    Converter for Collecting Gold Dust book.
    """

    def __init__(self, pdf_filename, structural_info):
        document = DocumentWithSubChapters(structural_info.book_title)
        ConverterBase.__init__(self, pdf_filename, document, structural_info)

    def breaks_document_into_chapters(self):
        return ConverterBase.breaks_document_into_chapters(
            self, ExtractedPage, SuperChapter
        )

    def _page_requires_paragraph_continuation(self, page_number):
        if self.structural_info._page_is_illustration(page_number):
            return False
        return ConverterBase._page_requires_paragraph_continuation(self, page_number)

    def _chapter_splitter(self):
        return self.structural_info.get_chapter_splitter()

    def sanitize_remove_header(self, extracted_page):
        if self._chapter_splitter().holds_new_chapter(extracted_page):
            # Chapters have no headers
            return

        header_less_page_text = extracted_page.text
        # Make sure the exact header text is encountered
        header_text = self.get_page_header(extracted_page)
        if not re.match("^" + header_text, header_less_page_text):
            print(
                "Header <<",
                header_text,
                ">> not found on pdf page ",
                extracted_page.page_number,
                " ",
                end="",
            )
            print(
                "(that is reader page number ",
                extracted_page.page_layout.reader_page_number,
                ")",
            )
            original_page_text = extracted_page.original_pdf_page.extract_text(
                extraction_mode="layout"
            )
            print("Pdf original text : ", repr(original_page_text))
            print("Exiting.")
            sys.exit()
        # Proceed with the removal of the header
        header_less_page_text = re.sub(header_text, "", header_less_page_text)
        extracted_page.set_removed_header(header_text)
        # Eventually, remove some possibly leaving whitespaces
        header_less_page_text = header_less_page_text.lstrip()
        # Eventually update the extracted_page
        extracted_page.text = header_less_page_text

    def sanitize_fix_illumination(self, extracted_page):
        """Chapters beginnings (that is the first page of a new chapter) start
        with an illumination (decorated first letter) that confuses pypdf.
        The letter of the illumination ends mixed up within the text of the
        first sentence of the chapter. Fix that.
        """
        page_number = extracted_page.page_number
        text_to_fix = extracted_page.text
        if not self._chapter_splitter().holds_new_chapter(extracted_page):
            print("Erroneous call to Converter::sanitize_fix_illumination()")
            print("  This extracted page does not seem to be a chapter starting page.")
            print("  Extracted page: ", extracted_page)
            print("  Exiting")
            sys.exit()

        delimiter = self.structural_info._get_chapter_info(page_number)[
            "illumination_delimiter"
        ]
        if delimiter is None:
            # This chapter has no illumination to fix (probably because there
            # is no illumination at all). Return the original text:
            return

        # The illumination character that got embedded in the text happens to
        # to always be preceded by a return character. Looking for the delimiter
        # prefixed with a return character will make the result a little more
        # secure (yet not foolproof):
        delimiter_with_return = "[\n]" + delimiter
        match = re.search(delimiter_with_return, text_to_fix)
        if not match:
            print(
                "Delimiter ",
                repr(delimiter),
                "not found within illumination for extracted page:",
            )
            print(extracted_page)
            print("Exiting.")
            sys.exit()
        if len(match.groups()) > 1:
            print(
                "Multiple occurrences of delimiter ",
                repr(delimiter),
                "within illumination for extracted page:",
            )
            print(extracted_page)
            print("Exiting.")
            sys.exit()

        # We shall only "fix" on the illumination concerned part of the text,
        # that is the text appearing before the delimiter. We thus split the
        # text in two parts:
        # - illumination_part: the part of the text that is prior to the
        #   delimiter and on which we shall proceed with modifications
        # - end_of_text: the remaining of the text that shall remain unchanged.
        illumination_part = text_to_fix[: match.end()]
        end_of_text = text_to_fix[match.end() :]

        # The first thing to do is to remove the illumination character from
        # the text. We use this opportunity to replace the return character,
        # that prefixed the delimiter, with a whitespace:
        corrected_snippet = delimiter[1:]
        illumination_part = re.sub(
            delimiter_with_return, " " + corrected_snippet, illumination_part
        )
        # The second thing to do is to reinsert the illumination character
        # within the text
        illumination_part = delimiter[0] + illumination_part
        # The third fix consists in removing the hand made spacing of the
        # beginning of the text (that would be overwritten by the illumination
        # drawing of the leading character):
        illumination_part = re.sub(
            self._chapter_splitter().chapter_name_separator_regex + "( *)",
            "",
            illumination_part,
        )
        # Eventually remove the occurrence (or the couple occurrences) of
        # returns + whitespaces that were added to reserve some space for the
        # illuminations on the second or third line of the text.
        # The following does work but goes too far...
        illumination_part = re.sub("(\n( *))", " ", illumination_part)

        # Eventually update the extracted_page
        extracted_page.text = illumination_part + end_of_text

    def sanitize_page_text(self, extracted_page):
        """
        After extraction of the text from the original pdf, some ad hoc
        manual cleaning is alas required e.g. remove the header of the page (when there is one).
        """
        self.sanitize_remove_header(extracted_page)
        if self._chapter_splitter().holds_new_chapter(extracted_page):
            self.sanitize_fix_illumination(extracted_page)

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
            + str(
                self.structural_info.convert_to_logical_page_number(
                    extracted_page.page_number
                )
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
            return str(self.structural_info.convert_to_logical_page_number(page_number))
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
                    + str(logical_page_number)
                    + str(logical_page_number)
                )
            else:
                # Even pages have a different header pattern based on the current
                # chapter name
                return self.chapter_page_header(extracted_page)

        WarnAndExit("Header for page number ", page_number, " is not defined")
