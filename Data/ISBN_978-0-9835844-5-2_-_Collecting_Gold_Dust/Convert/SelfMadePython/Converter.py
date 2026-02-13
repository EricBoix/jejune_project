import sys
import re
import os

sys.path.append(os.path.join("..", "..", "..", "ConvertPdfToMarkdown"))
from ConverterBase import ConverterBase
from Model import Chapter
from PageLayout import PageLayout
from ExtractedPage import ExtractedPage as ExtractedPageBase

import roman


class ExtractedPage(ExtractedPageBase):

    def set_removed_header(self, removed_header):
        self.removed_header = removed_header

    def __repr__(self):
        return (
            ExtractedPageBase.__repr__(self)
            + "\n"
            + "Removed header: "
            + repr(self.removed_header)
        )


class Converter(ConverterBase):
    """
    Converter for Collecting Gold Dust book.
    """

    def _page_requires_paragraph_continuation(self, page_number):
        if self.structural_info._page_is_illustration(page_number):
            return False
        return ConverterBase._page_requires_paragraph_continuation(self, page_number)

    def _get_page_number_finishing_last_paragraph(self, page_number):
        """
        A page that is followed by an illustration will need to skip that
        illustration page in order to retrieve the end of its last paragraph.
        Return the page number of the first page that defines a paragraph
        delimiter.
        """
        next_page_number = page_number + 1
        while self.structural_info._page_is_illustration(
            next_page_number
        ) or self._page_is_dropped(next_page_number):
            next_page_number += 1
        return next_page_number

    def remove_header(self, extracted_page):
        """
        The original pdf text of a page is polluted with the content of the
        header of the page, that varies from chapter names, the book name,
        the page number, a combination of the above ... or nothing.
        Clean up this mess.
        """
        original_page_text = extracted_page.original_pdf_page.extract_text(
            extraction_mode="layout"
        )

        # Remove the heading bunch of whitespaces (and assimilated characters)
        header_less_page_text = original_page_text.lstrip()
        # Make sure the exact header text is encountered
        header_text = self.structural_info.get_page_header(extracted_page.page_number)
        if not re.match("^" + header_text, header_less_page_text):
            print(
                "Header ",
                header_text,
                "not found on pdf page ",
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
        # When necessary fix chapter illumination
        page_number = extracted_page.page_number
        if self.structural_info._is_chapter_beginning_page(page_number):
            header_less_page_text = self.fix_illumination(
                page_number, header_less_page_text
            )

        extracted_page.text = header_less_page_text

    def build_chapters(self):
        resulting_chapters = []
        current_chapter = None
        for page_number in range(0, self.structural_info.total_page_number):

            if self._page_is_dropped(page_number):
                continue

            if self.structural_info._is_chapter_beginning_page(page_number):
                new_chapter_name = self.structural_info._get_chapter_name(page_number)
                current_chapter = Chapter(new_chapter_name)
                resulting_chapters.append(current_chapter)
            else:
                if not current_chapter:
                    # We didn't encounter a first chapter yet the first
                    # encountered page is not a page starting a chapter.
                    print("Any chapter must start with...a chapter typed page.")
                    print("Note: we didn't encounter the first chapter yet.")
                    print("Exiting")
                    sys.exit()

            ### Create a new extracted page:
            new_extracted_page_layout = PageLayout(
                self.structural_info.convert_to_logical_page_number(page_number),
                page_number,
            )
            new_extracted_page_layout.set_reference_text(
                "[Page: "
                + str(new_extracted_page_layout.reader_page_number)
                + " (page number: "
                + str(new_extracted_page_layout.page_number)
                + ")]"
            )
            new_extracted_page = ExtractedPage(
                page_number,
                new_extracted_page_layout,
                self.reader.pages[page_number],  # Original page
            )

            self.remove_header(new_extracted_page)
            current_chapter.add_page(new_extracted_page)

        for chapter in resulting_chapters:
            self.break_chapter_into_paragraphs(chapter)
            for paragraph in chapter.paragraphs:
                self.break_paragraph_into_sentences(paragraph)
        for chapter in resulting_chapters:
            self.reconstitute_paragraphs_spreading_over_two_pages(chapter)
        return resulting_chapters

    def fix_illumination(self, page_number, text_to_fix):
        """Chapters beginnings (that is the first page of a new chapter) start
        with an illumination (decorated first letter) that confuses pypdf.
        The letter of the illumination ends mixed up within the text of the
        first sentence of the chapter. Fix that.
        """
        if not self.structural_info._is_chapter_beginning_page(page_number):
            print("Erroneous call to Converter::fix_illumination()")
            print("  This does not seem to be a chapter starting page.")
            print("  Exiting")
            sys.exit()
        delimiter = self.structural_info.pages_info[page_number]["chapter_info"][
            "illumination_delimiter"
        ]
        if delimiter is None:
            # This chapter has no illumination to fix (probably because there
            # is no illumination at all). Return the original text:
            return text_to_fix
        # The illumination character that got embedded in the text happens to
        # to always be preceded by a return character. Looking for the delimiter
        # prefixed with a return character will make the result a little more
        # secure (yet not foolproof):
        delimiter_with_return = "[\n]" + delimiter
        if not re.search(delimiter_with_return, text_to_fix):
            print(
                "Delimiter ",
                repr(delimiter),
                "not found within illumination of chapter on page ",
                page_number,
                ".",
            )
            print(
                "Chapter text that we were looking to fix: ",
                repr(text_to_fix),
            )
            print("Exiting.")
            sys.exit()
        # The first thing to do is to remove the illumination character from
        # the text. We use this opportunity to replace the return character,
        # that prefixed the delimiter, with a whitespace:
        corrected_snippet = delimiter[1:]
        text_to_fix = re.sub(
            delimiter_with_return, " " + corrected_snippet, text_to_fix
        )
        # The second thing to do is to reinsert the illumination character
        # within the text
        text_to_fix = delimiter[0] + text_to_fix
        # The third fix consists in replacing the hand made spacing of the
        # first lines of the text (that would be overwritten by the illumination
        # drawing of the leading character) with a single white space:
        return re.sub("\n      ", " ", text_to_fix)

    def __page_has_paragraph_delimiter(self, page_number):
        if not page_number in self.structural_info.pages_info:
            return False
        if (
            not "first_paragraph_delimiter"
            in self.structural_info.pages_info[page_number]
        ):
            return False
        return True
