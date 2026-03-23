# A set of debugging utilities.

import pypdf


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
        print(page.extract_text())

    print("##########################################################")
    print("################## END OF RAW DOCUMENT ###################")
    print("##########################################################\n")


def print_document_pages(document):
    """
    Print the pages of the document.
    """
    print("##########################################################")
    print("##########################################################")
    print("############ DOCUMENT AS SET OF PAGES ####################")
    print("##########################################################")
    print("##########################################################\n")
    for chapter in document.get_chapters():
        print("#################################")
        print("################## Chapter name: ", chapter.name)
        print("#################################")
        for page in chapter.pages:
            print("################# Page content:")
            print(repr(page))
            print("")


def print_document_paragraphs(document):
    """
    Print the paragraphs of the document.
    """
    print("##########################################################")
    print("##########################################################")
    print("############ DOCUMENT AS SET OF PARAGRAPHS ###############")
    print("##########################################################")
    print("##########################################################\n")
    for chapter in document.chapters:
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


def print_document_chapter(chapter):
    print("###################################################################")
    print("################## Chapter name: ", chapter.name)
    print("###################################################################")
    for paragraph in chapter.get_paragraphs():
        print(
            "Paragraph (ref:",
            paragraph.get_reference(),
            ")",
        )
        for sentence in paragraph.get_sentences():
            print(
                "Sentence (ref:",
                sentence.page_layout.reference_text,
                "):\n",
                sentence.sentence,
                "\n",
            )


def print_document_sentences(document):
    """
    Print the paragraphs of the document.
    """
    print("##########################################################")
    print("##########################################################")
    print("##### DOCUMENT AS SET OF SENTENCES WITHIN PARAGRAPHS #####")
    print("##########################################################")
    print("##########################################################\n")
    for chapter in document.get_chapters():
        print_document_chapter(chapter)


def print_document_with_subchapter_sentences(document):
    """
    Print the document at the sentence level
    """
    print("##########################################################")
    print("##########################################################")
    print("############### DOCUMENT DOWN TO THE SENTENCES ###########")
    print("##########################################################")
    print("##########################################################\n")
    for superchapter in document.get_chapters():
        print("###################################################################")
        print("################## Super Chapter name: ", superchapter.name)
        print("###################################################################")
        for chapter in superchapter.get_chapters():
            print_document_chapter(chapter)
