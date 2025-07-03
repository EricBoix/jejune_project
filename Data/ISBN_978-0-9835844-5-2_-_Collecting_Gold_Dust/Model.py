from __future__ import annotations  # Allow forward references in type hints
from PageLayout import PageLayout
from mdutils.mdutils import MdUtils  # Added import
from typing import List, Optional


class Sentence:
    """
    A sentence _has_ a Layout (a page identifier for the reader to retrieve it)
    """

    def __init__(self, text: str, layout: PageLayout) -> None:
        self.sentence = text
        self.page_layout = layout.__copy__()

    def append(self, other: Sentence) -> None:
        """
        Append text to the current sentence.
        """
        self.sentence += " " + other.sentence

    def to_markdown(self, md_file: MdUtils) -> None:
        """
        Add this sentence's content to the given MdUtils object.
        """
        md_file.new_line(repr(self.sentence))


class Paragraph:
    """
    A list of sentences.
    """

    def __init__(self, layout: PageLayout) -> None:
        self.sentences: List[Sentence] = list()
        self.page_layout = layout

    def add_sentence(self, sentence: Sentence) -> None:
        self.sentences.append(sentence)

    def remove_sentence(self, sentence: Sentence) -> None:
        """
        Remove a sentence from the paragraph.
        """
        if sentence in self.sentences:
            self.sentences.remove(sentence)
        else:
            raise ValueError("Sentence not found in paragraph.")

    def concatenate(self, other: "Paragraph") -> None:
        """
        Concatenate another paragraph to this one.
        """
        self.sentences.extend(other.sentences)

    def to_markdown(self, md_file: MdUtils) -> None:
        """
        Add this paragraph's content to the given MdUtils object by calling each sentence's to_markdown.
        """
        # Note: we can not delegate the markdown generation to
        # Sentence.to_markdown() since we would have to use md_file.new_line()
        # which (as expected) adds an unwanted mandatory line break
        paragraph_as_text = " ".join([sentence.sentence for sentence in self.sentences])
        md_file.new_paragraph(paragraph_as_text)


class Chapter:
    """
    A list of Paragraphs.
    """

    def __init__(self, name: str) -> None:
        self.name: str = name
        # The original pages out of which this chapter is made
        self.pages: List[str] = list()
        # The paragraphs that got extracted from the pages
        self.paragraphs: List[Paragraph] = list()
        self.page_layout: Optional[PageLayout] = None

    def add_page(self, page) -> None:
        self.pages.append(page)

    def add_paragraph(self, new_paragraph: Paragraph) -> None:
        self.paragraphs.append(new_paragraph)

    def remove_paragraph(self, paragraph: Paragraph) -> None:
        """
        Remove a paragraph from the chapter.
        """
        if paragraph in self.paragraphs:
            self.paragraphs.remove(paragraph)
        else:
            raise ValueError("Paragraph not found in chapter.")

    def to_markdown(self, md_file: MdUtils) -> None:
        """
        Add this chapter's content to the given MdUtils object.
        """
        md_file.new_header(level=2, title=self.name)
        for paragraph in self.paragraphs:
            paragraph.to_markdown(md_file)


class Document:
    """
    A list of Chapters.
    """

    def __init__(self) -> None:
        self.chapters: List[Chapter] = []

    def add_chapter(self, new_chapter: Chapter) -> None:
        self.chapters.append(new_chapter)

    def to_markdown(self, filepath: str) -> None:
        """
        Generate a markdown file representing the document.
        """
        md_file = MdUtils(file_name=filepath, title="Document")
        md_file.new_header(level=1, title="DUMMY TITLE")
        for chapter in self.chapters:
            chapter.to_markdown(md_file)
        md_file.create_md_file()
