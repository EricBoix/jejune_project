import sys
import re

# To deal with inputs of the Converter class
from pypdf import PdfReader

# To deal with outputs of the Converter class
from Model import Document, Paragraph, Sentence

# To realize the conversion per se
import nltk

# Refer to
# https://stackoverflow.com/questions/78862426/unable-to-use-nltk-functions
nltk.download("punkt_tab")


class ConverterBase:
    """
    Class converting the original set of pages extracted from the pypdf::reader
    to a structured document. In order to realize its purpose the Converter
    needs to be manually provided with the structural information (extracted by
    a human reader) that must be promoted to the semantic structure (document,
    chapter, sub-chapter, paragraph...).
    """

    def __init__(self, pdf_filename, structural_info):

        # The original pdf document file name that this converter will act from
        self.pdf_filename = pdf_filename

        # The structural information constituted by the presence of chapters,
        # illustrations ... is quite often difficult to be automatically
        # discovered. While waiting for better (and free) tools, the following
        # was manually extracted
        self.structural_info = structural_info

        # Parse the pdf and make some basic coherence checks on the result:
        self.reader = PdfReader(self.pdf_filename)
        if len(self.reader.pages) != self.structural_info.total_page_number:
            print("Erroneous number of pages:")
            print(
                "Was expecting",
                self.structural_info.total_page_number,
                " but got ",
                len(self.reader.pages),
            )
            print("Exiting")
            sys.exit()
        for page_number in range(self.structural_info.total_page_number):
            self._assert_reader_page_number_is_coherent(page_number)

    def _assert_reader_page_number_is_coherent(self, page_number):
        # Slightly paranoid check on the reader numbering job coherence. When
        # given a page_number assert that the corresponding page wears that
        # very same page number (pretty dumb test BTW)
        original_reader_page = self.reader.pages[page_number]
        original_reader_page_number = self.reader.get_page_number(original_reader_page)
        if page_number != original_reader_page_number:
            print("Python page number does not match pypdf::reader page number:")
            print("   - Python page number: ", page_number)
            print("   - pypdf::reader page number: ", original_reader_page_number)
            print("Exiting.")
            sys.exit()
        return True

    def _page_is_dropped(self, page_number):
        if not page_number in self.structural_info.pages_info:
            return False
        if not "drop_page" in self.structural_info.pages_info[page_number]:
            return False
        return True

    def _page_requires_paragraph_continuation(self, page_number):
        if not page_number in self.structural_info.pages_info:
            return True  # Looks a bit ambitious but let's try it
        if "paragraph_fits_on_page" in self.structural_info.pages_info[page_number]:
            return False
        return True

    def _chapter_get_first_paragraph_of_given_page(self, chapter, page_number):
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

    def _chapter_get_last_paragraph_of_given_page(self, chapter, page_number):
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

    def get_document(self):
        """
        Return a Document object that holds the chapters and paragraphs
        """
        document = Document(self.structural_info.book_title)
        for chapter in self.build_chapters():
            document.add_chapter(chapter)
        return document

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

    def break_chapter_into_paragraphs(self, chapter):
        for page in chapter.pages:
            if not page.text:
                print("Warning: trying to breakdown a paragraph with NO text.")

            paragraphs = re.split(
                self.structural_info.chapter_to_paragraph_breaking_pattern, page.text
            )
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

    # Abstract methods to be implemented by subclasses

    def _get_page_number_finishing_last_paragraph(self, page_number):
        raise NotImplementedError(
            "Subclasses must implement _get_page_number_finishing_last_paragraph"
        )

    def reconstitute_paragraphs_spreading_over_two_pages(self, chapter):
        raise NotImplementedError(
            "Subclasses must implement reconstitute_paragraphs_spreading_over_two_pages"
        )

    def build_chapters(self):
        raise NotImplementedError("Subclasses must implement build_chapters")
