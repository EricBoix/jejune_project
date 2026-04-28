import sys
import pypdf
from .Model import (
    TopLevelChapterOfParagraphs,
    SubChapterOfParagraphs,
    SuperChapter,
    Paragraph,
)

_debug_mode = False


def set_debug_mode(enabled: bool):
    global _debug_mode
    _debug_mode = enabled


def Debug(message: str):
    if _debug_mode:
        print(message)


# A set of debugging utilities.


def print_document_raw_pages(pdf_filename):
    """
    Print the pages of the document.
    """
    reader = pypdf.PdfReader(pdf_filename)

    print("##########################################################")
    print("##########################################################")
    print("##### RAW DOCUMENT WITH A PAGE BASED BREAKDOWN ###########")
    print("##########################################################")
    print("##########################################################\n")
    print("Total number of pages: ", len(reader.pages))

    for page_number in range(len(reader.pages)):
        page = reader.pages[page_number]
        print("############### Page number ", page_number, "############")
        print(repr(page.extract_text(extraction_mode="layout")))

    print("##########################################################")
    print("################## END OF RAW DOCUMENT ###################")
    print("##########################################################\n")


class PrintDocument:
    def __init__(self, document):
        self._document = document

    def pages(self):
        print("##########################################################")
        print("##########################################################")
        print("############ DOCUMENT AS SET OF PAGES ####################")
        print("##########################################################")
        print("##########################################################\n")
        for chapter in self._document.get_chapters():
            print("#################################")
            print("################## Chapter name: ", chapter.name)
            print("#################################")
            for page in chapter.pages:
                print("################# Page content:")
                print(repr(page))
                print("")

    def paragraphs(self):
        print("##########################################################")
        print("##########################################################")
        print("############ DOCUMENT AS SET OF PARAGRAPHS ###############")
        print("##########################################################")
        print("##########################################################\n")
        for chapter in self._document.get_chapters():
            print("###################################################################")
            print("################## Chapter name: ", chapter.name)
            print("###################################################################")
            for paragraph in chapter.get_sublevels():
                print(
                    "Paragraph (ref:",
                    paragraph.get_document_reference_long(),
                    "):\n",
                    paragraph.text,
                    "\n",
                )

    def sentences(self):
        print("##########################################################")
        print("##########################################################")
        print("##### DOCUMENT AS SET OF SENTENCES WITHIN PARAGRAPHS #####")
        print("##########################################################")
        print("##########################################################\n")
        for chapter in self._document.get_chapters():
            self._print_chapter(chapter)

    def with_subchapter_sentences(self):
        print("##########################################################")
        print("##########################################################")
        print("############### DOCUMENT DOWN TO THE SENTENCES ###########")
        print("##########################################################")
        print("##########################################################\n")
        for superchapter in self._document.get_chapters():
            print("###################################################################")
            print("################## Super Chapter name: ", superchapter.name)
            print("###################################################################")
            for sublevel in superchapter.get_sublevels():
                if isinstance(
                    sublevel, (TopLevelChapterOfParagraphs, SubChapterOfParagraphs)
                ):
                    self._print_chapter(sublevel)
                elif isinstance(sublevel, Paragraph):
                    self._print_paragraph_and_sentences(sublevel)

    def _print_chapter(self, chapter):
        if isinstance(chapter, SuperChapter):
            self._print_super_chapter(chapter)
            return
        if isinstance(chapter, (TopLevelChapterOfParagraphs, SubChapterOfParagraphs)):
            self._print_chapter_of_paragraphs(chapter)

    def _print_super_chapter(self, super_chapter):
        if not isinstance(super_chapter, SuperChapter):
            print("Chapter ", super_chapter.name, "is not a SuperChapter.")
            print("Exiting.")
            sys.exit()
        print("###################################################################")
        print("################## Super Chapter name: ", super_chapter.name)
        print("###################################################################")
        for sublevel in super_chapter.get_sublevels():
            if isinstance(
                sublevel, (TopLevelChapterOfParagraphs, SubChapterOfParagraphs)
            ):
                self._print_chapter_of_paragraphs(sublevel)
                continue
            if isinstance(sublevel, Paragraph):
                self._print_paragraph_and_sentences(sublevel)
                continue
            print("Chapter ", super_chapter.name, "is of unknown type.")
            print("Exiting.")
            sys.exit()

    def _print_chapter_of_paragraphs(self, chapter):
        if not isinstance(
            chapter, (TopLevelChapterOfParagraphs, SubChapterOfParagraphs)
        ):
            print("Chapter ", chapter.name, "is not a ChapterOfParagraphs.")
            print("Exiting.")
            sys.exit()
        print("###################################################################")
        print("################## Chapter name: ", chapter.name)
        print("###################################################################")
        for paragraph in chapter.get_sublevels():
            self._print_paragraph_and_sentences(paragraph)

    def _print_paragraph_and_sentences(self, paragraph):
        print("###", paragraph.get_document_reference_long())
        sentences = paragraph.get_sentences()
        if not sentences:
            print("PARAGRAPH IS EMPTY OF SENTENCES")
            return
        for sentence in sentences:
            print(
                f"{sentence.text} \n   [Reference: {sentence.get_document_reference_long()}]"
            )
