import pypdf
from .Model import ChapterOfParagraphs, Paragraph

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
        for chapter in self._document.chapters:
            print("###################################################################")
            print("################## Chapter name: ", chapter.name)
            print("###################################################################")
            for paragraph in chapter.paragraphs:
                print(
                    "Paragraph (ref:",
                    paragraph.get_reference(),
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
                if isinstance(sublevel, ChapterOfParagraphs):
                    self._print_chapter(sublevel)
                elif isinstance(sublevel, Paragraph):
                    self._print_paragraph_and_sentences(sublevel)

    def _print_chapter(self, chapter):
        print("###################################################################")
        print("################## Chapter name: ", chapter.name)
        print("###################################################################")
        for paragraph in chapter.get_paragraphs():
            self._print_paragraph_and_sentences(paragraph)

    def _print_paragraph_and_sentences(self, paragraph):
        print("### Paragraph (ref:", paragraph.get_reference(), ")")
        sentences = paragraph.get_sentences()
        if not sentences:
            print("PARAGRAPH IS EMPTY OF SENTENCES")
            return
        for sentence in sentences:
            print(
                sentence.page_layout.reference_text,
                ":\n",
                sentence.text,
                "\n",
            )
