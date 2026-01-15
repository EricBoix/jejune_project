import sys
import re
import os

# To deal with inputs of the Converter class
from pypdf import PdfReader

# To deal with outputs of the Converter class
from Model import Document, Chapter, Paragraph, Sentence
from PageLayout import PageLayout

# To realize the conversion per se
import PageInfo
import nltk

# Refer to
# https://stackoverflow.com/questions/78862426/unable-to-use-nltk-functions
nltk.download("punkt_tab")


class ExtractedPage:
    """
    Representation of a pdf extracted page
    Attributes
    ----------
    page_number: int
        The index of the page as it appears extracted by pydf::PdfReader()
    original_pdf_page: str
        the text as original extracted by the constructor caller
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
            + "Original Text: "
            + repr(self.original_pdf_page.extract_text(extraction_mode="layout"))
            + "\n"
            + "Extracted text: "
            + repr(self.text)
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
        # CLEAN ME : they are no headers anymore
        self.book_title = "COLLECTING GOLD DUST: Nurturing the Dhamma in Daily Living"

        # This number of pages is already known (will assert it later on)
        self.total_page_number = PageInfo.total_page_number

        # The structural information constituted by the presence of chapters,
        # illustrations ... is quite often difficult to be automatically
        # discovered. While waiting for better (and free) tools, the following
        # was manually extracted
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
        while self.__page_is_illustration(next_page_number):
            print(
                "Skipping illustration of page number ",
                next_page_number,
                " while looking for the content of the end of the paragraph",
            )
            print("that starts on page number  ", page_number, ".")
            next_page_number += 1
        return next_page_number

    def __is_chapter_beginning_page(self, page_number):
        if not page_number in self.pages_info:
            return False
        if self.pages_info[page_number]["type"] == "chapter":
            return True
        return False

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

    def __assert_chapter_name(self, page_number, beginning_page):
        if not self.__get_chapter_name(page_number):
            print("The assumption that page number ", page_number)
            print(" start a chapter was incorrect. ")
            print("Exiting.")
            sys.exit()
        if not "chapter_info" in self.pages_info[page_number]:
            print("Chapter page without chapter_info (page number ", page_number, ").")
            print("Exiting")
            sys.exit()
        if not "name" in self.pages_info[page_number]["chapter_info"]:
            print(
                "chapter_info of chapter page without name (page number ",
                page_number,
                ").",
            )
            print("Exiting")
            sys.exit()
        chapter_name = self.pages_info[page_number]["chapter_info"]["name"]
        if not re.search(chapter_name + "[\n\n\n]", beginning_page.text):
            print(
                "Chapter page (page number ",
                page_number,
                ") does not seem to start with ",
                chapter_name,
                ".",
            )
            print("Exiting.")
            sys.exit()

    def __convert_to_logical_page_number(self, page_number):
        if page_number == 0:
            return "Cover"
        # Just making sure
        original_reader_page = self.reader.pages[page_number]
        original_reader_page_number = self.reader.get_page_number(original_reader_page)
        if page_number != original_reader_page_number:
            print("Python page number does not match pypdf::reader page number:")
            print("   - Python page number: ", page_number)
            print("   - pypdf::reader page number: ", original_reader_page_number)
            print("Exiting.")
            sys.exit()
        return page_number

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
            if not page.text:
                print("FIXME FIXME: WARNING, this page has NO text !?")
                print("Exiting.")
                sys.exit()

            paragraphs = re.split("\n   ", page.text)
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
        When a page ends with an unfinished Paragraph then the next page begins
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

    def define_sanitized_text(self, extracted_page):
        """
        After extraction of the text from the original pdf, some ad hoc
        manual cleaning is alas required.
        """
        original_page_text = extracted_page.original_pdf_page.extract_text(
            extraction_mode="layout"
        )

        # For some undocumented reason the pdfreader output has "\t" characters
        # instead of whitespaces. Brutally convert those tabulations to
        # whitespaces
        sanitized_page_text = re.sub("\\t", " ", original_page_text)

        # Remove the heading bunch of whitespaces (and assimilated characters)
        sanitized_page_text = sanitized_page_text.lstrip()

        extracted_page.text = sanitized_page_text

    def build_chapters(self):
        resulting_chapters = []
        current_chapter = Chapter("Preamble")
        resulting_chapters.append(current_chapter)
        for page_number in range(0, self.total_page_number):

            if self.__is_chapter_beginning_page(page_number):
                new_chapter_name = self.__get_chapter_name(page_number)
                current_chapter = Chapter(new_chapter_name)
                resulting_chapters.append(current_chapter)

            if self.__page_is_dropped(page_number):
                continue

            ### Create a new extracted page:
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

            self.define_sanitized_text(new_extracted_page)
            current_chapter.add_page(new_extracted_page)

            ### Now that the chapter has some content assert it's name is
            # the one documented in PageInfo
            if self.__is_chapter_beginning_page(page_number):
                self.__assert_chapter_name(page_number, new_extracted_page)

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
