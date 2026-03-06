import sys
import re

# To deal with inputs of the Converter class
from pypdf import PdfReader

# To deal with outputs of the Converter class
from .Model import Document
from .Model import Paragraph, Sentence, Chapter
from .PageLayout import PageLayout

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

        # The result of the conversion process
        self.document = Document(self.structural_info.book_title)

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

        # Eventually realize the conversion
        self.build_document()

    def build_chapters(self, ExtractedPageDerived):
        resulting_chapters = []
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
                "[Page: "
                + str(new_extracted_page_layout.reader_page_number)
                + " (page number: "
                + str(new_extracted_page_layout.page_number)
                + ")]"
            )
            # The usage of ExtractedPage, that can be a derived class, prevents
            # the declaration of this member function to be done in the parent
            # class. This is because although all derived classes with define
            # exactly the same function definition, the concrete ExtractedPage
            # class type might (and thus will) differ from one derivation of
            # a converter to another one.
            new_extracted_page = ExtractedPageDerived(
                page_number,
                new_extracted_page_layout,
                self.reader.pages[page_number],  # Original page
            )

            self.sanitized_page_text(new_extracted_page)

            ### Is this new extracted page the beginning of a chapter ?
            # Either the extracted page has this knowledge or we rely on
            # the structural_info provided hint
            if new_extracted_page.is_chapter_beginning_page():
                new_chapter_name = new_extracted_page.get_chapter_name()
            elif self.structural_info._is_chapter_beginning_page(page_number):
                new_chapter_name = self.structural_info._get_chapter_name(page_number)
            else:
                new_chapter_name = None  # Not a new chapter
                if not current_chapter:
                    # We didn't encounter a first chapter yet the first
                    # encountered page is not a page starting a chapter.
                    print("Any chapter must start with...a chapter typed page.")
                    print("Note: we didn't encounter the first chapter yet.")
                    print("Exiting")
                    sys.exit()

            if new_chapter_name is not None:
                # Some chapter names include newline characters that must be
                # sanitized in order to create a proper new Chapter object:
                sanitized_new_chapter_name = re.sub("\n", " ", new_chapter_name)
                current_chapter = Chapter(sanitized_new_chapter_name)
                resulting_chapters.append(current_chapter)
                # Yet what we must extracted is the "un-sanitized" chapter name
                new_extracted_page.extract_chapter_name(new_chapter_name)

            current_chapter.add_page(new_extracted_page)

        for chapter in resulting_chapters:
            self.break_chapter_into_paragraphs(chapter)
            for paragraph in chapter.paragraphs:
                self.break_paragraph_into_sentences(paragraph)
        for chapter in resulting_chapters:
            self.reconstitute_paragraphs_spreading_over_two_pages(chapter)
        return resulting_chapters

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

    def build_document(self):
        """
        Build the Document object out of converter extracted chapters
        """
        for chapter in self.build_chapters():
            self.document.add_chapter(chapter)

    def get_document(self):
        return self.document

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
            if not self._page_requires_paragraph_continuation(page_number):
                continue
            next_page_number = (
                self.structural_info._get_page_number_finishing_last_paragraph(
                    page_number
                )
            )
            if self.structural_info._is_chapter_beginning_page(next_page_number):
                # The next page is the starting page of a new chapter. This
                # implies that the current page is the last page of this
                # chapter which is thus complete. There is hence nothing to be
                # collected from the next page
                continue

            ill_ending_paragraph = self._chapter_get_last_paragraph_of_given_page(
                chapter, page_number
            )
            ill_starting_paragraph = self._chapter_get_first_paragraph_of_given_page(
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
