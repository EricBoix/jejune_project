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
        self._owning_chapter: Chapter = None
        # Paragraph number within owning chapter. Note that paragraphs numbering
        # is for human consumption and thus starts at 1, not 0.
        self._number: int = None
        self.page_layout = layout

    @property
    def number(self) -> Optional[int]:
        return self._number

    @property
    def owning_chapter(self) -> Chapter:
        return self._owning_chapter

    def set_owning_chapter(self, chapter: Chapter) -> None:
        """
        Set the chapter that owns this paragraph.
        """
        self._owning_chapter = chapter

    def set_number(self, number: int) -> None:
        self._number = number

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

    def merge(self, other: "Paragraph") -> None:
        """
        Concatenate another paragraph to this one and dispose of the other.
        This method assumes that the other paragraph is from the same chapter.
        """
        if self._owning_chapter != other._owning_chapter:
            raise ValueError("Cannot concatenate paragraphs from different chapters.")
        self.sentences.extend(other.sentences)
        self._owning_chapter.remove_paragraph(other)
        self._owning_chapter.renumber_paragraphs()

    def get_reference(self) -> str:
        # A reference within the document for human consumption.
        return (
            "Paragraph "
            + str(self._number)
            + " of chapter "
            + repr(self.owning_chapter.name)  # Just to add parentheses
            + ", page "
            + str(self.page_layout.reader_page_number)
            + " (index page number "
            + str(self.page_layout.page_number)
            + ")"
        )

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

    def renumber_paragraphs(self) -> None:
        for index, paragraph in enumerate(self.paragraphs, start=1):
            paragraph.set_number(index)

    def to_markdown(self, md_file: MdUtils) -> None:
        """
        Add this chapter's content to the given MdUtils object.
        """
        md_file.new_header(level=1, title=self.name)
        for paragraph in self.paragraphs:
            paragraph.to_markdown(md_file)
        md_file.new_line()


class Document:
    """
    A list of Chapters.
    """

    def __init__(self, title) -> None:
        self.chapters: List[Chapter] = []
        self.title = title

    def add_chapter(self, new_chapter: Chapter) -> None:
        self.chapters.append(new_chapter)

    def to_markdown(self, filepath: str) -> None:
        """
        Generate a markdown file representing the document.
        """
        md_file = MdUtils(file_name=filepath, title=self.title)
        for chapter in self.chapters:
            chapter.to_markdown(md_file)
        # Appending a "table a content" makes the Markdown to Pdf conversion
        # fail. This is because (well inquire on that) converting the table of
        # contents requires converting has markdown links (things of the
        # form "[some name](#some-name-tag)") and resolving them, when they
        # do not exist in the text:
        #    md_file.new_table_of_contents(table_title="Contents", depth=2)
        md_file.create_md_file()
