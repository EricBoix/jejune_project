# A set of debugging utilities.


def print_document_pages(document):
    """
    Print the pages of the document.
    """
    print("##########################################################")
    print("##########################################################")
    print("############ DOCUMENT AS SET OF PAGES ####################")
    print("##########################################################")
    print("##########################################################\n")
    for chapter in document.chapters:
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


def print_document_sentences(document):
    """
    Print the paragraphs of the document.
    """
    print("##########################################################")
    print("##########################################################")
    print("##### DOCUMENT AS SET OF SENTENCES WITHIN PARAGRAPHS #####")
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
                ")",
            )
            for sentence in paragraph.sentences:
                print(
                    "Sentence (ref:",
                    sentence.page_layout.reference_text,
                    "):\n",
                    sentence.sentence,
                    "\n",
                )
