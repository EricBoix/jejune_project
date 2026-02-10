import sys
import re
import os

# To deal with inputs of the Converter class
from pypdf import PdfReader

# To deal with outputs of the Converter class
sys.path.append(os.path.join("..", "..", "..", "ConvertPdfToMarkdown"))
from Model import Document, Chapter, Paragraph, Sentence
from PageLayout import PageLayout
from ExtractedPage import ExtractedPage as ExtractedPageBase

# To realize the conversion per se
import PageInfo
import roman
import nltk

# Refer to
# https://stackoverflow.com/questions/78862426/unable-to-use-nltk-functions
nltk.download("punkt_tab")


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


class Converter:
    """
    Class converting the original set of pages extracted from the pypdf::reader
    to a structured document. In order to realize its purpose the Converter
    needs to be manually provided with the structural information (extracted by
    a human reader) that must be promoted to the semantic structure (document,
    chapter, sub-chapter, paragraph...).
    """

    def __init__(self, pdf_filename):

        # The original pdf document file name that this converter will act from
        self.pdf_filename = pdf_filename

        # The original pdf document has a title. This title ends-up embedded in
        # some headers of the pages and must be extracted from the text.
        self.book_title = "COLLECTING GOLD DUST: Nurturing the Dhamma in Daily Living"

        # This number of pages is already known (will assert it later on)
        self.total_page_number = PageInfo.total_page_number

        # The preamble section pages use roman numbering. This offsets the numbering
        # of the body pages
        self.page_numbering_offset = PageInfo.page_numbering_offset

        # The structural information constituted by the presence of chapters,
        # illustrations, illumination, headers ... is quite often difficult
        # to be automatically discovered. While waiting for better (and free)
        # tools, the following is a manually extracted.
        self.pages_info = PageInfo.pages_info

        # Technical (optimisation) variable used to hold the correspondance
        # between a given page number and the chapter to which that page
        # belongs to. In other terms for this dictionary
        #  - a key is a page number
        #  - the associated value holds the current chapter number for that key
        self.__chapter_page = {}

        self.reader = PdfReader(self.pdf_filename)
        if len(self.reader.pages) != self.total_page_number:
            print("Erroneous number of pages:")
            print(
                "Was expecting",
                self.total_page_number,
                " but got ",
                len(self.reader.pages),
            )
            print("Exiting")
            sys.exit()

    def __page_is_illustration(self, page_number):
        if not page_number in self.pages_info:
            return False
        if not "type" in self.pages_info[page_number]:
            print("Page with no known type (page number ", page_number, ").")
            print("Exiting")
            sys.exit()
        if self.pages_info[page_number]["type"] == "illustration":
            return True
        return False

    def __page_is_dropped(self, page_number):
        if not page_number in self.pages_info:
            return False
        if not "drop_page" in self.pages_info[page_number]:
            return False
        return True

    def __page_requires_paragraph_continuation(self, page_number):
        if not page_number in self.pages_info:
            return True  # Looks a bit ambitious but let's try it
        if self.__page_is_illustration(page_number):
            return False
        if "paragraph_fits_on_page" in self.pages_info[page_number]:
            return False
        return True

    def __get_page_number_finishing_last_paragraph(self, page_number):
        """
        A page that is followed by an illustration will need to skip that
        illustration page in order to retrieve the end of its last paragraph.
        Return the page number of the first page that defines a paragraph
        delimiter.
        """
        next_page_number = page_number + 1
        while not self.__page_has_paragraph_delimiter(next_page_number):
            if not self.__page_is_illustration(next_page_number):
                print(
                    "Oddly enough we are on page number ",
                    page_number,
                    " and we are looking for the page holding the content of the end of the paragraph.",
                )
                print("Yet page number ", next_page_number, " is not an illustration.")
                print("How could this be?")
                print(
                    "Maybe we forgot to define the first_paragraph_delimiter of page number ",
                    next_page_number,
                    "?",
                )
                print("Exiting.")
                sys.exit()
            next_page_number += 1
        return next_page_number

    def __page_has_paragraph_delimiter(self, page_number):
        if not page_number in self.pages_info:
            return False
        if not "first_paragraph_delimiter" in self.pages_info[page_number]:
            return False
        return True

    def __get_first_paragraph_delimiter(self, page_number):
        """
        Return the delimiting string (delimiter) the end of the paragraph that
        started on the previous page and finishes on page with the page number page_number
        """
        if not self.__page_has_paragraph_delimiter(page_number):
            print("How is it that were a looking for an unknown delimiter?")
            print("Exiting")
            sys.exit()
        return self.pages_info[page_number]["first_paragraph_delimiter"]

    def __is_chapter_beginning_page(self, page_number):
        if not page_number in self.pages_info:
            return False
        if self.pages_info[page_number]["type"] == "chapter":
            return True
        return False

    def __book_title_page_header(self, page_number):
        return (
            str(self.__convert_to_logical_page_number(page_number))
            + r" \| "
            + self.book_title
        )

    def __chapter_page_header(self, page_number):
        return (
            self.__get_chapter_name(page_number)
            + r" \| "
            + str(self.__convert_to_logical_page_number(page_number))
        )

    def __initialize_chapter_page(self):
        if bool(self.__chapter_page):
            # Already initialized
            return
        current_chapter_page = None
        for page_number in range(0, self.total_page_number):
            if self.__is_chapter_beginning_page(page_number):
                current_chapter_page = page_number
            self.__chapter_page[page_number] = current_chapter_page

    def __get_chapter_page(self, page_number):
        self.__initialize_chapter_page()
        return self.__chapter_page[page_number]

    def __get_chapter_name(self, page_number):
        chapter_page = self.__get_chapter_page(page_number)
        return self.pages_info[chapter_page]["chapter_info"]["name"]

    def __convert_to_logical_page_number(self, page_number):
        if page_number == 0:
            return "Cover"
        # Deal with the first pages numbering that uses roman numeration
        if page_number >= 1 and page_number <= 17:
            return roman.toRoman(page_number).lower()
        # Just making sure
        original_reader_page = self.reader.pages[page_number]
        original_reader_page_number = self.reader.get_page_number(original_reader_page)
        if page_number != original_reader_page_number:
            print("Python page number does not match pypdf::reader page number:")
            print("   - Python page number: ", page_number)
            print("   - pypdf::reader page number: ", original_reader_page_number)
            print("Exiting.")
            sys.exit()
        return page_number - self.page_numbering_offset

    def fix_illumination(self, page_number, text_to_fix):
        """Chapters beginnings (that is the first page of a new chapter) start
        with an illumination (decorated first letter) that confuses pypdf.
        The letter of the illumination ends mixed up within the text of the
        first sentence of the chapter. Fix that.
        """
        if not self.__is_chapter_beginning_page(page_number):
            print("Erroneous call to Converter::fix_illumination()")
            print("  This does not seem to be a chapter starting page.")
            print("  Exiting")
            sys.exit()
        delimiter = self.pages_info[page_number]["chapter_info"][
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

    def __is_headless_page(self, page_number):
        # Only illustrations can be headless
        if not self.__page_is_illustration(page_number):
            return False
        # Yet some illustrations still have a header
        if "header" in self.pages_info[page_number]:
            return False
        # Eventually illustrations not flagged as having a header are headless
        return True

    def __get_page_header(self, page_number):

        if page_number < 0 or page_number > self.total_page_number:
            print("Page number is outside of book page numeration.")
            print("Exiting")
            sys.exit()

        # Pages explicitly flagged as headless, well, are headless:
        if self.__is_headless_page(page_number):
            return ""

        # First headers of pages starting a new chapter have that new
        # chapter name as header
        if self.__is_chapter_beginning_page(page_number):
            return self.__get_chapter_name(page_number)

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
            return str(self.__convert_to_logical_page_number(page_number))
        if page_number <= 19 and page_number <= 21:
            return ""

        ####### Concerning the body of the book.
        # Pages of the body of the book, have a headers that follow a simple
        # constructive rule with some exceptions...

        if (page_number % 2) == 0:
            # Odd pages have a header that is simply the book title followed
            # by their page number
            return self.__book_title_page_header(page_number)
        if (page_number % 2) != 0:
            if page_number == 133:
                # Page 133 has a brain damaged header that doesn't
                # follow the even page header rule (although it is a near miss). The
                # only possible fix is to define an exception:
                return (
                    self.book_title
                    + self.__get_chapter_name(133)
                    + " ||"
                    + str(self.__convert_to_logical_page_number(133))
                    + str(self.__convert_to_logical_page_number(133))
                )
            else:
                # Even pages have a different header pattern based on the current
                # chapter name
                return self.__chapter_page_header(page_number)

        print("Header for page number ", page_number, " is not defined")
        print("Exiting")
        sys.exit()

    def __chapter_get_first_paragraph_of_given_page(self, chapter, page_number):
        for paragraph in chapter.paragraphs:
            if paragraph.page_layout.page_number == page_number:
                return paragraph
        print(
            "Error: unable to find the first paragraph of page number ",
            page_number,
            " in chapter ",
            chapter.name,
        )
        print("Exiting.")
        sys.exit()

    def __chapter_get_last_paragraph_of_given_page(self, chapter, page_number):
        paragraph_of_that_page = None
        for paragraph in chapter.paragraphs:
            if paragraph.page_layout.page_number == page_number:
                paragraph_of_that_page = paragraph
        if paragraph_of_that_page is None:
            print(
                "Error: unable to find the last paragraph of page number ",
                page_number,
                " in chapter ",
                chapter.name,
            )
            print("Exiting.")
            sys.exit()
        return paragraph_of_that_page

    def sanitize_newlines_and_multiple_whitespaces(self, input_text):

        # Newlines are encountered to denote different usages
        #  - set some tabulations of illuminations (example "\       ")
        #  - define a new paragraph in which case newline is followed by
        #    exactly 4 whitespaces (example "\n    "): refer to
        #    break_chapter_into_paragraphs() method
        #  - simple line folding within original paragraphs or even sentences
        #    were newline are used to format the original pdf with lines returns.
        # Remove such formatting characters to preserve only the text content:
        result = re.sub("\n", " ", input_text)

        # HISTORICAL NOTES: for some long forgot reason, and when development
        # stage was centered on pages (as opposed to paragraphs), there was a
        # need for removing the  newline characters ("\n") but only when they
        # were preceded or followed either by a single whitespace or some
        # character (examples "here\nand", "here \nand", "here\n and"). Because
        # finding the proper regex to do so was quite difficult, the following
        # keeps track of the sub() call, in case it is needed later on.
        # The regexp logic is that we need to use both lookbehind and lookahead
        # notations and can be understood as: look for a newline preceded
        # (?<=...)  by any character that is not an extended whitespace (\s)
        # and followed (?=[^\s]) by any character that is not a whitespace:
        #    result_text = re.sub("(?<=[^\s])\n(?=[^\s])", " ", input_text)

        # The above clean-up might create multiple whitespaces, while some
        # other occurrences of multiple whitespaces are (randomly?) encountered.
        # Remove them all:
        result = re.sub(r"\s+", " ", result).strip()
        return result

    def break_chapter_into_paragraphs(self, chapter):
        for page in chapter.pages:
            # TODO: the second pattern of the split() method happens on
            # sub-chapter beginnings. Instead of simply starting a new paragraph
            # we should start a new sub-chapter!
            paragraphs = re.split("\n    " + "|" + "\n\n\n", page.text)
            page_layout = page.page_layout
            for paragraph_text in paragraphs:
                if len(paragraph_text) == 0:
                    # Avoid creating empty paragraphs (resulting from previous
                    # erroneous/careless string manipulations):
                    continue
                new_paragraph_layout = page_layout.__copy__()
                new_paragraph_layout.set_reference_text(
                    "[Chapter: "
                    + chapter.name
                    + ", reader page number: "
                    + str(page_layout.reader_page_number)
                    + ", page number: "
                    + str(page_layout.page_number)
                    + "]"
                )
                new_paragraph = Paragraph(new_paragraph_layout)
                new_paragraph.set_owning_chapter(chapter)
                # Note: the text member is a temporary attribute used by the
                # Converter but is not destined to be a member of the Paragraph
                # class. We just piggyback it until it is transformed and
                # cleaned-up.
                new_paragraph.text = paragraph_text
                chapter.add_paragraph(new_paragraph)
        chapter.renumber_paragraphs()

    def break_paragraph_into_sentences(self, paragraph: Paragraph):
        paragraph_layout = paragraph.page_layout

        # Using the text attribute that was piggybacked from the above
        # break_chapter_into_paragraphs() method:
        if paragraph.text is None:
            print(
                "Error: trying to break a paragraph into sentences but "
                "the paragraph text is None."
            )
            print("Exiting.")
            sys.exit()
        paragraph_text = paragraph.text
        tokenized_text = nltk.tokenize.sent_tokenize(paragraph_text)
        for new_sentence_text in tokenized_text:
            if len(new_sentence_text) == 0:
                # Avoid creating empty sentences (resulting from previous
                # erroneous/careless string manipulations):
                continue

            # Eventually, create a new sentence
            new_sentence_layout = paragraph_layout.__copy__()
            new_sentence_layout.set_reference_text(
                "[Sentence: on reader page number: "
                + str(paragraph_layout.reader_page_number)
                + " within "
                + paragraph_layout.reference_text
                + "]"
            )
            new_sentence_text = self.sanitize_newlines_and_multiple_whitespaces(
                new_sentence_text
            )
            new_sentence = Sentence(new_sentence_text, new_sentence_layout)
            paragraph.add_sentence(new_sentence)

    def reconstitute_paragraphs_spreading_over_two_pages(self, chapter):
        """
        When a page ends with un unfinished Paragraph then the next page begins
        with the end of that Paragraph. In order to reconstitute such Paragraphs
        that were split in two, we need to
         - find the last Paragraph of a page that is not annotated with the
           "paragraph_fits_on_page" flag. Such a Paragraph holds the beginning
            of an original paragraph that got split in two.
         - the next Paragraph thus holds the end of the original paragraph
           (that got split in two) and
           - was standing at the top of the next page
           - contains a paragraph delimiter.
         - merge those two paragraphs into a single Paragraph
         - when doing so make sure that the sentence that got split (and was
           standing over two ill reconstituted Paragraphs) gets also properly
           reconstituted.
        """
        if len(chapter.pages) == 1:
            # Nothing to do for a single page
            return
        for page_index in range(0, len(chapter.pages) - 1):
            current_page = chapter.pages[page_index]
            page_number = current_page.page_number
            if not self.__page_requires_paragraph_continuation(page_number):
                continue
            next_page_number = self.__get_page_number_finishing_last_paragraph(
                page_number
            )
            if not self.__page_has_paragraph_delimiter(next_page_number):
                # The page was explicitly stated as no to be treated. Skip it.
                continue
            if self.__is_chapter_beginning_page(next_page_number):
                # The next page is the starting page of a new chapter. This
                # implies that the current page is the last page of this
                # chapter which is thus complete. There is hence nothing to be
                # collected from the next page
                continue

            ill_ending_paragraph = self.__chapter_get_last_paragraph_of_given_page(
                chapter, page_number
            )
            ill_starting_paragraph = self.__chapter_get_first_paragraph_of_given_page(
                chapter, next_page_number
            )

            #### Asserting some preconditions before merging the two paragraphs:

            # Assert that the page_layout of the two paragraphs do differ
            if ill_ending_paragraph.page_layout == ill_starting_paragraph.page_layout:
                print(
                    "Error: the page layout of the two paragraphs to be merged is the same.",
                    "This is not expected.",
                )
                print(
                    "Paragraph ending on page number ",
                    page_number,
                    " has page layout ",
                    repr(ill_ending_paragraph.page_layout),
                )
                print(
                    "Paragraph starting on page number ",
                    next_page_number,
                    " has page layout ",
                    repr(ill_starting_paragraph.page_layout),
                )
                print("Exiting.")
                sys.exit()

            # Assert that the ill_starting_paragraph is indeed the one that
            # holds the prescribed delimiter:
            last_sentence_of_ill_starting_paragraph = ill_starting_paragraph.sentences[
                -1
            ]
            delimiter = self.__get_first_paragraph_delimiter(next_page_number)
            if not re.search(
                delimiter, last_sentence_of_ill_starting_paragraph.sentence
            ):
                print(
                    "Error: the last sentence of the paragraph starting on page number ",
                    next_page_number,
                    " does not end with the delimiter ",
                    repr(delimiter),
                )
                print("Last sentence: ", repr(last_sentence_of_ill_starting_paragraph))
                print("Exiting.")
                sys.exit()

            #### Proceed with the merging of two paragraphs into a single one:
            first_sentence_of_ill_starting_paragraph = ill_starting_paragraph.sentences[
                0
            ]
            last_sentence_of_ill_ending_paragraph = ill_ending_paragraph.sentences[-1]
            # First merge the two sentences:
            last_sentence_of_ill_ending_paragraph.append(
                first_sentence_of_ill_starting_paragraph
            )
            ill_starting_paragraph.remove_sentence(
                first_sentence_of_ill_starting_paragraph
            )
            # Then merge the two paragraphs:
            ill_ending_paragraph.merge(ill_starting_paragraph)

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
        header_text = self.__get_page_header(extracted_page.page_number)
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
        if self.__is_chapter_beginning_page(page_number):
            header_less_page_text = self.fix_illumination(
                page_number, header_less_page_text
            )

        extracted_page.text = header_less_page_text

    def build_chapters(self):
        resulting_chapters = []
        current_chapter = Chapter("Preamble")
        resulting_chapters.append(current_chapter)
        for page_number in range(0, self.total_page_number):
            if self.__page_is_dropped(page_number):
                continue

            if self.__is_chapter_beginning_page(page_number):
                new_chapter_name = self.__get_chapter_name(page_number)
                current_chapter = Chapter(new_chapter_name)
                resulting_chapters.append(current_chapter)

            # Create a new extracted page:
            new_extracted_page_layout = PageLayout(
                self.__convert_to_logical_page_number(page_number), page_number
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

    def get_document(self):
        """
        Return a Document object that holds the chapters and paragraphs
        """
        document = Document(self.book_title)
        for chapter in self.build_chapters():
            document.add_chapter(chapter)
        return document
