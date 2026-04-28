from typing import Callable, List, Optional, Protocol, Tuple

from .Model import (
    DocumentHierarchicalLevel,
    SubChapterOfParagraphs,
    Paragraph,
)
from .PageLayout import PageLayout
from .Warning import Warning, WarnAndExit
from .Traces import Debug


class Splitter(Protocol):
    """Protocol for level splitters."""

    def split(self, content_text: str) -> List[str]: ...
    def get_sublevel_name(self, content_text: str) -> Optional[str]: ...


class ContentWithLayout(Protocol):
    """Protocol for content with page layout."""

    text: str
    page_layout: PageLayout


class LevelBreaker:
    """
    Breaks a DocumentHierarchicalLevel into sublevels using a splitter.
    Extracted from ConverterBase to simplify the code structure.
    """

    def __init__(
        self,
        level: DocumentHierarchicalLevel,
        level_splitter: Splitter,
        sublevel_factory: Callable[[Optional[PageLayout]], DocumentHierarchicalLevel],
        break_level_callback: Callable[[DocumentHierarchicalLevel], None],
        break_paragraphs_callback: Callable[
            [DocumentHierarchicalLevel, Optional[List[ContentWithLayout]]], None
        ],
    ):
        self.level = level
        self.level_splitter = level_splitter
        self.sublevel_factory = sublevel_factory
        self.break_level = break_level_callback
        self.break_paragraphs = break_paragraphs_callback

    def break_into_sublevels(
        self, contents: Optional[List[ContentWithLayout]] = None
    ) -> None:
        """Break a hierarchical level into sublevels using the provided splitter."""
        Debug(f"########### break_into_sublevels, level: {self.level}")

        if not contents:
            contents = self.level.get_text_with_layout()
            if not contents:
                Warning(f"DocumentHierarchicalLevel {self.level} with NO text content.")

        current_level = self.level
        for level_content in contents:
            content_text = level_content.text
            Debug(f"####### break_into_sublevels, contents: {content_text}")
            if not content_text:
                Warning(f"level with NO text.")
                continue

            content_layout = level_content.page_layout
            new_layout = content_layout.__copy__()

            parts = self.level_splitter.split(content_text)
            while parts:
                Debug(f"### break_into_sublevels, ({len(parts)}) parts: {parts}")

                new_sublevel, parts = self._try_create_sublevel(new_layout, parts)
                if new_sublevel:
                    current_level = new_sublevel
                    continue

                should_break, parts = self._handle_unbreakable_text(
                    new_layout, current_level, parts
                )
                if should_break:
                    break

    def _try_create_sublevel(
        self, new_layout: PageLayout, parts: List[str]
    ) -> Tuple[Optional[DocumentHierarchicalLevel], List[str]]:
        """Try to create a sublevel from parts[0] (name) and parts[1] (content).
        Returns (new_sublevel, remaining_parts) tuple."""
        if len(parts) < 2:
            return None, parts
        new_sublevel_name = self.level_splitter.get_sublevel_name(parts[0])
        if not new_sublevel_name:
            return None, parts
        new_sublevel = self.sublevel_factory(new_layout)
        new_sublevel.set_name(new_sublevel_name)
        new_sublevel.append_text(parts[1])
        self.break_level(new_sublevel)
        self.level.add_sublevel(new_sublevel)
        return new_sublevel, parts[2:]

    def _handle_unbreakable_text(
        self,
        new_layout: PageLayout,
        current_level: DocumentHierarchicalLevel,
        parts: List[str],
    ) -> Tuple[bool, List[str]]:
        """Handle text that cannot be broken into sublevels.
        Returns (should_break, remaining_parts) tuple."""
        new_sublevel_type = type(self.sublevel_factory(None))
        remaining = parts[1:]

        if new_sublevel_type == Paragraph:
            new_paragraph = Paragraph(new_layout)
            new_paragraph.append_text(parts[0])
            self.break_level(new_paragraph)
            current_level.add_sublevel(new_paragraph)
            return False, remaining

        if new_sublevel_type == SubChapterOfParagraphs:
            # Create a Paragraph directly in the SuperChapter instead of
            # a ChapterOfParagraphs containing a single paragraph.
            class ParagraphContent:
                pass

            ParagraphContent.page_layout = new_layout
            ParagraphContent.text = parts[0]
            self.break_paragraphs(current_level, [ParagraphContent])
            return (not remaining), remaining

        WarnAndExit(
            f"Expected Paragraph or ChapterOfParagraphs, got {new_sublevel_type}"
        )
        return False, parts
