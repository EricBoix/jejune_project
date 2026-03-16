from __future__ import annotations  # Allow forward references in type hints
from abc import ABC
import sys
from .PageLayout import PageLayout
from mdutils.mdutils import MdUtils  # Added import
from typing import Generic, List, Optional, TypeVar, TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Protocol

    class HasToMarkdown(Protocol):
        def to_markdown(self, md_file: MdUtils) -> None: ...

# Type variable for sublevel types in DocumentHierarchicalLevel
T = TypeVar("T", bound="DocumentHierarchicalLevel | None")


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


class DocumentHierarchicalLevel(ABC, Generic[T]):
    """
    A chapter, a sub-chapter, a sub-sub-chapter, with an optional list of sublevels.
    The type parameter T specifies the allowed sublevel type.
    """

    def __init__(self, name: str) -> None:
        self.name: str = name
        # The original pages out of which this level will be made up
        self.pages: List[str] = list()
        # The optional sub-hierarchical levels of this one
        self.sublevels: Optional[List[T]] = None
        # The page where this Hierarchical level is encountered within the
        # original document
        self.page_layout: Optional[PageLayout] = None
        # Header level for markdown output (set by subclasses)
        self.level: int = 0

    def add_page(self, page) -> None:
        if not self.pages:
            self.page_layout = page.page_layout
        self.pages.append(page)

    def add_sublevel(self, sublevel: T) -> None:
        if not self.sublevels:
            self.sublevels = list()
        self.sublevels.append(sublevel)

    def get_sublevel(self, index: int) -> T:
        if not self.sublevels or index >= len(self.sublevels):
            print("Sublevel index ", index, " out of bounds ", end="")
            print("(should be smaller than ", len(self.sublevels) if self.sublevels else 0, ")")
            sys.exit()
        return self.sublevels[index]

    def remove_sublevel(self, sublevel: T) -> None:
        """
        Remove a sublevel from this hierarchical level.
        """
        if self.sublevels and sublevel in self.sublevels:
            self.sublevels.remove(sublevel)
        else:
            raise ValueError("Sublevel not found.")

    def to_markdown(self, md_file: MdUtils) -> None:
        """
        Add this hierarchical level's content to the given MdUtils object.
        """
        md_file.new_header(level=self.level, title=self.name, add_table_of_contents="n")
        if self.sublevels:
            for sublevel in self.sublevels:
                if sublevel is not None:
                    sublevel.to_markdown(md_file)
        md_file.new_line()


class Paragraph(DocumentHierarchicalLevel[None]):
    """
    A list of sentences. Lowest level in the document hierarchy.
    Sentence is a leaf and not a DocumentHierarchicalLevel.
    """

    def __init__(self, layout: PageLayout) -> None:
        DocumentHierarchicalLevel.__init__(self, name="")
        self.sentences: List[Sentence] = list()
        self._owning_hierarchical_level: Optional[SubChapter] = None
        # Paragraph number within owning subchapter. Note that paragraphs numbering
        # is for human consumption and thus starts at 1, not 0.
        self._number: Optional[int] = None
        self.page_layout = layout
        self.level = 4

    @property
    def number(self) -> Optional[int]:
        return self._number

    @property
    def owning_hierarchical_level(self) -> Optional[SubChapter]:
        return self._owning_hierarchical_level

    def set_owning_hierarchical_level(self, subchapter: SubChapter) -> None:
        """
        Set the subchapter that owns this paragraph.
        """
        self._owning_hierarchical_level = subchapter

    # Keep old method name for backwards compatibility
    def set_owning_chapter(self, chapter: SubChapter) -> None:
        self.set_owning_hierarchical_level(chapter)

    def set_number(self, number: int) -> None:
        self._number = number

    def add_sentence(self, sentence: Sentence) -> None:
        self.sentences.append(sentence)

    def get_sentence(self, sentence_number: int) -> Sentence:
        if sentence_number > len(self.sentences):
            print("Sentence index ", sentence_number, " out of bounds ", end="")
            print("(should be smaller than ", len(self.sentences), ")")
            sys.exit()
        return self.sentences[sentence_number]

    def remove_sentence(self, sentence: Sentence) -> None:
        """
        Remove a sentence from the paragraph.
        """
        if sentence in self.sentences:
            self.sentences.remove(sentence)
        else:
            raise ValueError("Sentence not found in paragraph.")

    def merge(self, other: Paragraph) -> None:
        """
        Concatenate another paragraph to this one and dispose of the other.
        This method assumes that the other paragraph is from the same subchapter.
        """
        if self._owning_hierarchical_level != other._owning_hierarchical_level:
            raise ValueError("Cannot concatenate paragraphs from different subchapters.")
        if self._owning_hierarchical_level is None:
            raise ValueError("Paragraph has no owning hierarchical level.")
        self.sentences.extend(other.sentences)
        self._owning_hierarchical_level.remove_paragraph(other)
        self._owning_hierarchical_level.renumber_paragraphs()

    def get_reference(self) -> str:
        # A reference within the document for human consumption.
        owner_name = self.owning_hierarchical_level.name if self.owning_hierarchical_level else "unknown"
        page_reader = self.page_layout.reader_page_number if self.page_layout else "?"
        page_num = self.page_layout.page_number if self.page_layout else "?"
        return (
            "Paragraph "
            + str(self._number)
            + " of subchapter "
            # Just to add parentheses
            + repr(owner_name)
            + ", page "
            + str(page_reader)
            + " (index page number "
            + str(page_num)
            + ")"
        )

    def to_markdown(self, md_file: MdUtils) -> None:
        """
        Add this paragraph's content to the given MdUtils object.
        Overrides base class to output sentences instead of sublevels.
        """
        # Note: we can not delegate the markdown generation to
        # Sentence.to_markdown() since we would have to use md_file.new_line()
        # which (as expected) adds an unwanted mandatory line break
        paragraph_as_text = " ".join([sentence.sentence for sentence in self.sentences])
        md_file.new_paragraph(paragraph_as_text)


class SubChapter(DocumentHierarchicalLevel[Paragraph]):
    def __init__(self, name: str) -> None:
        DocumentHierarchicalLevel.__init__(self, name)
        self.level = 3

    def add_paragraph(self, paragraph: Paragraph) -> None:
        paragraph.set_owning_hierarchical_level(self)
        self.add_sublevel(paragraph)

    def remove_paragraph(self, paragraph: Paragraph) -> None:
        self.remove_sublevel(paragraph)

    def renumber_paragraphs(self) -> None:
        if self.sublevels:
            for index, paragraph in enumerate(self.sublevels, start=1):
                paragraph.set_number(index)

    def to_markdown(self, md_file: MdUtils) -> None:
        """Output subchapter content; skip header if this is a default (unnamed) subchapter."""
        if self.name:
            md_file.new_header(level=self.level, title=self.name, add_table_of_contents="n")
        if self.sublevels:
            for paragraph in self.sublevels:
                paragraph.to_markdown(md_file)
        if self.name:
            md_file.new_line()


class Chapter(DocumentHierarchicalLevel[SubChapter]):
    def __init__(self, name: str) -> None:
        DocumentHierarchicalLevel.__init__(self, name)
        self.level = 2
        self._default_subchapter: Optional[SubChapter] = None

    def add_subchapter(self, subchapter: SubChapter) -> None:
        self.add_sublevel(subchapter)

    def _get_or_create_default_subchapter(self) -> SubChapter:
        """Get or create a default subchapter to hold paragraphs when no explicit subchapters exist."""
        if self._default_subchapter is None:
            self._default_subchapter = SubChapter("")
            self._default_subchapter.page_layout = self.page_layout
            self.add_sublevel(self._default_subchapter)
        return self._default_subchapter

    def add_paragraph(self, paragraph: Paragraph) -> None:
        """Add paragraph to the default subchapter (convenience method for backward compatibility)."""
        subchapter = self._get_or_create_default_subchapter()
        subchapter.add_paragraph(paragraph)

    def remove_paragraph(self, paragraph: Paragraph) -> None:
        """Remove paragraph from the default subchapter (convenience method for backward compatibility)."""
        if self._default_subchapter:
            self._default_subchapter.remove_paragraph(paragraph)

    def renumber_paragraphs(self) -> None:
        """Renumber paragraphs in all subchapters."""
        if self.sublevels:
            for subchapter in self.sublevels:
                subchapter.renumber_paragraphs()

    @property
    def paragraphs(self) -> List[Paragraph]:
        """Return all paragraphs from the default subchapter (backward compatibility)."""
        if self._default_subchapter and self._default_subchapter.sublevels:
            return self._default_subchapter.sublevels
        return []


class Document:
    """
    A list of Chapters.
    """

    def __init__(self, title) -> None:
        self.chapters: List[Chapter] = []
        self.title = title

    def add_chapter(self, new_chapter: Chapter) -> None:
        self.chapters.append(new_chapter)

    def get_chapters(self):
        return self.chapters

    def get_chapter_name(self, page_number):
        for chapter in self.chapters:
            if chapter.page_layout.page_number == page_number:
                return chapter.name
        print("Warning: chapter with pages number ", page_number, "not found.")
        return None

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
