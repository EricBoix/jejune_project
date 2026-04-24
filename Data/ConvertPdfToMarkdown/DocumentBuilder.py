from abc import ABC, abstractmethod
from typing import List, Optional, Protocol

import nltk

from .Model import (
    ChapterOfParagraphs,
    DocumentHierarchicalLevel,
    DocumentHierarchicalRoot,
    SuperChapter,
    Paragraph,
    Sentence,
)
from .PageLayout import PageLayout
from .StructuralInfoBase import StructuralInfoBase
from .Warning import WarnAndExit
from .LevelBreaker import LevelBreaker
from .TextSanitizer import TextSanitizer
from .ParagraphMerger import ParagraphMerger

nltk.download("punkt_tab", quiet=True)


class ContentWithLayout(Protocol):
    """Protocol for content with page layout."""

    text: str
    page_layout: PageLayout


class DocumentBuilder(TextSanitizer, ABC):
    """Builds document hierarchy by breaking levels into sublevels."""

    def __init__(
        self, document: DocumentHierarchicalRoot, structural_info: StructuralInfoBase
    ) -> None:
        self.document = document
        self.structural_info = structural_info
        self._paragraph_merger = ParagraphMerger(structural_info)

    def build_document(self) -> None:
        """Build the Document object out of converter extracted chapters."""
        self.break_document_into_chapters()  # Calling the derived version
        for chapter in self.document.get_chapters():
            self.break_level(chapter)
        for top_level_chapter in self.document.get_chapters():
            self._paragraph_merger.reconstitute_paragraphs_spreading_over_two_pages(
                top_level_chapter
            )

    @abstractmethod
    def break_document_into_chapters(self) -> None:
        """Break document into chapters. Must be implemented by subclass."""
        pass

    def break_paragraph_into_sentences(self, paragraph: Paragraph) -> None:
        paragraph_layout = paragraph.page_layout

        if paragraph.text is None:
            WarnAndExit(
                "Error: trying to break a paragraph into sentences but "
                "the paragraph text is None."
            )
        paragraph_text = paragraph.text
        tokenized_text = nltk.tokenize.sent_tokenize(paragraph_text)
        for new_sentence_text in tokenized_text:
            if not new_sentence_text:
                continue

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
            paragraph.add_sublevel(new_sentence)

    def break_any_level_chapter_into_paragraphs(
        self, chapter, contents: Optional[List[ContentWithLayout]] = None
    ) -> None:
        """The chapter argument can be of any level e.g. a SuperChapter or a ChapterOfParagraphs..."""
        breaker = LevelBreaker(
            level=chapter,
            level_splitter=self.structural_info.chapter_to_paragraph_splitter(),
            sublevel_factory=Paragraph,
            reference_prefix="Chapter",
            break_level_callback=self.break_level,
            break_paragraphs_callback=self.break_any_level_chapter_into_paragraphs,
        )
        breaker.break_into_sublevels(contents)
        chapter.renumber_paragraphs()

    def break_superchapter_into_chapters(self, chapter: SuperChapter) -> None:
        def chapter_of_paragraph_factory(layout: PageLayout) -> ChapterOfParagraphs:
            chapter_of_paragraph = ChapterOfParagraphs("")
            chapter_of_paragraph.page_layout = layout
            return chapter_of_paragraph

        breaker = LevelBreaker(
            level=chapter,
            level_splitter=self.structural_info.superchapter_to_chapter_splitter(),
            sublevel_factory=chapter_of_paragraph_factory,
            reference_prefix="Sub-Chapter",
            break_level_callback=self.break_level,
            break_paragraphs_callback=self.break_any_level_chapter_into_paragraphs,
        )
        breaker.break_into_sublevels()
        chapter.renumber_chapters()

    def break_level(self, level: DocumentHierarchicalLevel) -> None:
        LEVEL_HANDLERS = {
            Paragraph: self.break_paragraph_into_sentences,
            ChapterOfParagraphs: self.break_any_level_chapter_into_paragraphs,
            SuperChapter: self.break_superchapter_into_chapters,
        }
        handler = LEVEL_HANDLERS.get(type(level))
        if handler:
            handler(level)
            return
        WarnAndExit(f"Level of type {type(level)} has no break handler.")

    def break_sublevels(self, level: DocumentHierarchicalLevel) -> None:
        """Assuming this level was already broken into sublevels, recurse the breaking on its sublevels"""
        sublevels = level.get_sublevels()
        if not sublevels:
            WarnAndExit("Level without sublevels. Nothing to be done.")
            return
        for sublevel in sublevels:
            self.break_level(sublevel)
