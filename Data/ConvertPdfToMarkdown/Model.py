from __future__ import annotations  # Allow forward references in type hints
from abc import ABC
from typing import Generic, List, Optional, TypeVar, TYPE_CHECKING
import re
import nltk
from mdutils.mdutils import MdUtils

# Ensure NLTK data is available (downloads once if missing)
for resource, path in [
    ("punkt_tab", "tokenizers/punkt_tab"),
    ("averaged_perceptron_tagger_eng", "taggers/averaged_perceptron_tagger_eng"),
]:
    try:
        nltk.data.find(path)
    except LookupError:
        nltk.download(resource, quiet=True)
from .PageLayout import PageLayout
from .Warning import Warning, WarnAndExit


if TYPE_CHECKING:
    from typing import Protocol

    class HasToMarkdown(Protocol):
        def to_markdown(self, md_file: MdUtils) -> None: ...


# Type variable for sublevel types in DocumentHierarchicalLevel
T = TypeVar("T", bound="DocumentHierarchicalLevel | None")


class Numbered:
    def __init__(self) -> None:
        # Numbering of this hierarchical level is the position within the
        # container of the owning hierarchical level. Note that this numbering
        # is for human consumption and thus starts at 1, not 0.
        self._number: Optional[int] = None

    @property
    def number(self) -> Optional[int]:
        return self._number

    def set_number(self, number: int) -> None:
        self._number = number


class Parent:
    """Reference to a higher level within a hierarchy."""

    def __init__(self) -> None:
        self._owning_hierarchical_level = None

    def set_owning_hierarchical_level(self, parent) -> None:
        self._owning_hierarchical_level = parent

    @property
    def owning_hierarchical_level(self) -> Optional[DocumentHierarchicalLevel]:
        return self._owning_hierarchical_level

    @property
    def hierarchical_toplevel(self) -> Optional[DocumentHierarchicalLevel]:
        level = self
        while level.owning_hierarchical_level:
            level = level.owning_hierarchical_level
        return level


class Sentence(Numbered, Parent):
    """
    A sentence _has_ a Layout (a page identifier for the reader to retrieve it)
    """

    def __init__(self, text: str, layout: PageLayout) -> None:
        self.text = text
        self.page_layout = layout.__copy__()

    def append(self, other: Sentence) -> None:
        """
        Append text to the current sentence.
        """
        self.text += " " + other.text

    def is_complete(self):
        # The problem is hard, refer e.g. to
        # https://stackoverflow.com/questions/71590785/nlp-check-if-a-detected-sentence-is-a-complete-sentence
        # We check:
        # - starts with a capital letter
        # - ends with punctuation
        # - contains a verb (using NLTK POS tagging)
        if not self.text[0].isupper():
            return False
        if not bool(re.search(r"[.!?]$", self.text)):
            return False
        tokens = nltk.word_tokenize(self.text)
        tagged = nltk.pos_tag(tokens)
        has_verb = any(tag.startswith("VB") for _, tag in tagged)
        return has_verb

    def to_markdown(self, md_file: MdUtils, dummy_level) -> None:
        """
        Add this sentence's content to the given MdUtils object.
        """
        md_file.new_line(repr(self.text))

    def get_document_reference_long(self) -> str:
        # Paragraphs are nameless so we must grab the grand-parent
        owner_name = (
            self.owning_hierarchical_level.owning_hierarchical_level.name
            if self.owning_hierarchical_level
            else "unknown"
        )
        paragraph_number = (
            self.owning_hierarchical_level.number
            if self.owning_hierarchical_level
            else "unknown"
        )
        page_reader = self.page_layout.reader_page_number if self.page_layout else "?"

        return f"Source document: {self.hierarchical_toplevel.get_title()}, Chapter: {owner_name}, paragraph number {paragraph_number}, sentence number {self._number} on page {page_reader}"


class DocumentHierarchicalLevel(ABC, Generic[T], Numbered, Parent):
    """
    A chapter, a sub-chapter, a sub-sub-chapter, with an optional list of sublevels.
    The type parameter T specifies the allowed sublevel type.
    """

    def __init__(self, name: str) -> None:
        Parent.__init__(self)
        self.name: str = name
        if not self.name:
            Warning("DocumentHierarchicalLevel created with no given name.")
        # The text capturing this level as extracted from the original document.
        # Note that this text is only used in order to construct this model
        # during the hierarchical breakdown. Eventually all the text content
        # will end up (copied) in the Sentence (leaves of the hierarchy) or
        # intermediate level titles (e.g. chapter title)
        self.text: str = None
        # The optional sub-hierarchical levels of this one
        self.sublevels: Optional[List[T]] = None
        # The page where this Hierarchical level is encountered within the
        # original document
        self.page_layout: Optional[PageLayout] = None

    def get_text_with_layout(self):
        # Used to get some (artificial) genericity with DocumentHierarchicalRoot
        # where the original document text is stored in pages that have both
        # a text and a layout_page attribute.
        return [self]

    def add_sublevel(self, sublevel: T) -> None:
        if not self.sublevels:
            self.sublevels = list()
        self.sublevels.append(sublevel)
        sublevel.set_owning_hierarchical_level(self)

    def get_sublevel(self, index: int) -> T:
        if not self.sublevels or index >= len(self.sublevels):
            WarnAndExit(
                f"Sublevel index {index} out of bounds: should be smaller than {len(self.sublevels) if self.sublevels else 0}"
            )
        return self.sublevels[index]

    def get_last_sublevel(self):
        if not self.sublevels:
            Warning("No sublevels found.")
            return None
        return self.sublevels[-1]

    def remove_sublevel(self, sublevel: T) -> None:
        """
        Remove a sublevel from this hierarchical level.
        """
        if self.sublevels and sublevel in self.sublevels:
            self.sublevels.remove(sublevel)
        else:
            raise ValueError("Sublevel not found.")

    def get_sublevels(self):
        return self.sublevels

    def set_name(self, name: str) -> None:
        self.name = name

    def append_text(self, text: str) -> None:
        if self.text:
            self.text += text
        else:
            self.text = text

    def renumber_sublevels(self) -> None:
        if self.sublevels:
            for index, sublevel in enumerate(self.sublevels, start=1):
                sublevel.set_number(index)

    def has_page_number(self, page_number):
        return self.page_layout.page_number == page_number

    def get_first_sublevel_of_given_page(self, page_number):
        for sublevel in self.sublevels:
            if sublevel.page_layout.page_number == page_number:
                return sublevel
        Warning(
            f"unable to find the first sublevel of page number {page_number} in hierarchy {self.name}"
        )
        return None

    def get_last_sublevel_of_given_page(self, page_number):
        sublevel_of_that_page = None
        for sublevel in self.sublevels:
            if sublevel.page_layout.page_number == page_number:
                sublevel_of_that_page = sublevel
        if sublevel_of_that_page is None:
            Warning(
                f"unable to find the last sublevel of page number {page_number} in hierarchy {self.name}"
            )
        return sublevel_of_that_page

    def merge(self, other: DocumentHierarchicalLevel) -> None:
        """
        Concatenate another DocumentHierarchicalLevel to this one and dispose
        of the other. This method assumes that this instance and the other DocumentHierarchicalLevel both share the same hierarchical parent.
        """
        if type(self) is not type(other):
            WarnAndExit("Cannot merge two different types.")
        if self.owning_hierarchical_level != other.owning_hierarchical_level:
            if type(self.owning_hierarchical_level) is not type(
                other.owning_hierarchical_level
            ):
                # We should inquire further but we are probably in the case
                # where:
                #  - self and other are both paragraphs
                #  - type(parent(self)) is a SuperChapter
                #  - type(parent(other)) is a ChapterOfParagraph (that belongs
                #    to the same SuperChapter)
                # Although the paragraphs follow themselves, they do not share
                # the same parent (but the same grand-parent).
                Warning(f"Choosing not to merge {self} and {other}, because")
                Warning(f"their respective parent are of different types, that")
                Warning(
                    f"are {type(self.owning_hierarchical_level)} and {type(other.owning_hierarchical_level)}."
                )
                return
            else:
                Warning(
                    f"Choosing not to merge {self} from page {self.page_layout.page_number} and {other} from page {other.page_layout.page_number}, because they are not siblings."
                )
                return
        if self.owning_hierarchical_level is None:
            WarnAndExit("DocumentHierarchicalLevel has no owning hierarchical level.")
        self.sublevels.extend(other.sublevels)
        self.owning_hierarchical_level.remove_sublevel(other)
        self.owning_hierarchical_level.renumber_sublevels()

    def to_markdown(self, md_file: MdUtils, level) -> None:
        """
        Add this hierarchical level's content to the given MdUtils object.
        """
        if not self.name:
            WarnAndExit("No name for markdown conversion.")
        md_file.new_header(
            level=level,
            title=self.name,
            add_table_of_contents="n",
        )
        if self.sublevels:
            for sublevel in self.sublevels:
                if sublevel is not None:
                    sublevel.to_markdown(md_file, level + 1)
        md_file.new_line()


class Paragraph(DocumentHierarchicalLevel[Sentence]):
    """
    A list of sentences. Lowest level in the document hierarchy.
    Sentence is a leaf and not a DocumentHierarchicalLevel.
    """

    def __init__(self, layout: PageLayout) -> None:
        """A paragraph is a set of sentences"""
        DocumentHierarchicalLevel.__init__(self, name="Paragraph")
        self.page_layout = layout

    remove_sentence = DocumentHierarchicalLevel.remove_sublevel
    get_sentences = DocumentHierarchicalLevel.get_sublevels

    def get_document_reference_long(self) -> str:
        # A reference within the document for human consumption.
        owner_name = (
            self.owning_hierarchical_level.name
            if self.owning_hierarchical_level
            else "unknown"
        )
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

    def to_markdown(self, md_file: MdUtils, dummy_level) -> None:
        """
        Add this paragraph's content to the given MdUtils object.
        Overrides base class to output sentences instead of sublevels.
        """
        sentences = self.get_sublevels()
        if not sentences:
            print("FIXME FIXME FIXME FIXME FIXME")
            Warning("Useless paragraph with no sentences.")
            Warning("Optimisation inquiry required.")
            return
        # Note: we can not delegate the markdown generation to
        # Sentence.to_markdown() since we would have to use md_file.new_line()
        # which (as expected) adds an unwanted mandatory line break
        paragraph_as_text = " ".join([sentence.text for sentence in sentences])
        md_file.new_paragraph(paragraph_as_text)


class TopLevelChapter:
    def __init__(self) -> None:
        # The original pages of the document constituting this chapter
        self.pages: List[str] = list()

    def add_page(self, page) -> None:
        if not self.pages:
            self.page_layout = page.page_layout
        self.pages.append(page)

    def get_text_with_layout(self):
        return self.pages


class TopLevelChapterOfParagraphs(
    TopLevelChapter, DocumentHierarchicalLevel[Paragraph]
):
    """Chapter with pages, used as direct children of Document."""

    def __init__(self, name: str) -> None:
        DocumentHierarchicalLevel.__init__(self, name)
        TopLevelChapter.__init__(self)

    def get_text_with_layout(self):
        return self.pages

    def get_document_reference_long(self) -> str:
        """A reference within the document for human consumption."""
        owner_name = (
            self.owning_hierarchical_level.name
            if self.owning_hierarchical_level
            else "unknown"
        )
        page_reader = self.page_layout.reader_page_number if self.page_layout else "?"
        page_num = self.page_layout.page_number if self.page_layout else "?"
        return (
            "Chapter "
            + str(self._number)
            + repr(owner_name)
            + ", page "
            + str(page_reader)
            + " (index page number "
            + str(page_num)
            + ")"
        )


class SubChapterOfParagraphs(DocumentHierarchicalLevel[Paragraph]):
    """Sub-chapter with text, used as children of SuperChapter."""

    def __init__(self, name: str) -> None:
        DocumentHierarchicalLevel.__init__(self, name)

    def get_text_with_layout(self):
        return [self]

    def get_document_reference_long(self) -> str:
        """A reference within the document for human consumption."""
        owner_name = (
            self.owning_hierarchical_level.name
            if self.owning_hierarchical_level
            else "unknown"
        )
        page_reader = self.page_layout.reader_page_number if self.page_layout else "?"
        page_num = self.page_layout.page_number if self.page_layout else "?"
        return (
            "SubChapter "
            + str(self._number)
            + repr(owner_name)
            + ", page "
            + str(page_reader)
            + " (index page number "
            + str(page_num)
            + ")"
        )


class SuperChapter(TopLevelChapter, DocumentHierarchicalLevel[SubChapterOfParagraphs]):
    def __init__(self, name: str) -> None:
        DocumentHierarchicalLevel.__init__(self, name)
        TopLevelChapter.__init__(self)

    add_chapter = DocumentHierarchicalLevel.add_sublevel
    remove_chapter = DocumentHierarchicalLevel.remove_sublevel
    get_chapters = DocumentHierarchicalLevel.get_sublevels
    renumber_chapters = DocumentHierarchicalLevel.renumber_sublevels

    def is_SuperChapterOfParagraph(self):
        if not self.get_sublevels():
            # We can not really decide.
            return False
        some_sublevel = self.get_last_sublevel()
        if isinstance(some_sublevel, Paragraph):
            return True
        return False


class DocumentHierarchicalRoot:
    """
    A list of Chapters.
    """

    def __init__(self, title) -> None:
        self.title = title

    def get_title(self) -> str:
        return self.title

    def get_chapter_name(self, page_number):
        chapter = self.get_first_sublevel_of_given_page(page_number)
        if chapter:
            return chapter.name
        Warning(f"chapter with page number {page_number} not found.")
        return None

    def to_markdown(self, filepath: str) -> None:
        """
        Generate a markdown file representing the document.
        """
        md_file = MdUtils(
            file_name=filepath, title=self.title, title_header_style="atx"
        )
        for chapter in self.get_chapters():
            chapter.to_markdown(md_file, level=2)
        # Appending a "table a content" makes the Markdown to Pdf conversion
        # fail. This is because (well inquire on that) converting the table of
        # contents requires converting markdown links (things of the form
        # "[some name](#some-name-tag)") and resolving them, when they
        # do not exist in the text:
        #    md_file.new_table_of_contents(table_title="Contents", depth=2)
        md_file.create_md_file()


class Document(
    DocumentHierarchicalRoot, DocumentHierarchicalLevel[TopLevelChapterOfParagraphs]
):
    def __init__(self, title: str) -> None:
        DocumentHierarchicalRoot.__init__(self, title)
        DocumentHierarchicalLevel.__init__(self, "Document")

    add_chapter = DocumentHierarchicalLevel.add_sublevel
    get_chapters = DocumentHierarchicalLevel.get_sublevels


class DocumentWithSubChapters(
    DocumentHierarchicalRoot, DocumentHierarchicalLevel[SuperChapter]
):
    def __init__(self, title: str) -> None:
        DocumentHierarchicalRoot.__init__(self, title)
        DocumentHierarchicalLevel.__init__(self, "DocumentWithSubChapters")

    add_chapter = DocumentHierarchicalLevel.add_sublevel
    get_chapters = DocumentHierarchicalLevel.get_sublevels
