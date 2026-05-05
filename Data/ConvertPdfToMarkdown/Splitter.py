import re
from typing import Optional, Protocol

from .Warning import Warning, WarnAndExit


class ChapterSplitter:
    """Top level splitter, that is chapter boundary."""

    def __init__(
        self,
        structural_info,
        separator_regex,
        extractor_regex,
        separator_first_occurrence,
    ):
        self.structural_info = structural_info
        self.separator_regex = separator_regex
        self.extractor_regex = extractor_regex
        self.separator_first_occurrence = separator_first_occurrence

    def holds_new_chapter(self, extracted_page) -> bool:
        # First check static declaration in pages_info
        if self.structural_info._holds_new_chapter(extracted_page.page_number):
            return True
        # Then check regex pattern
        match = re.search(self.separator_regex, extracted_page.text)
        if not match:
            return False
        if match.start() > self.separator_first_occurrence:
            return False
        return True

    def get_chapter_name(self, extracted_page) -> Optional[str]:
        # First check static declaration in pages_info
        if self.structural_info._holds_new_chapter(extracted_page.page_number):
            return self.structural_info._get_chapter_name(extracted_page.page_number)
        # Then use regex extraction
        chapter_name = re.split(self.extractor_regex, extracted_page.text)
        if not chapter_name:
            WarnAndExit(
                f"Chapter name {chapter_name} not found in extracted page {extracted_page.text}"
            )
        return chapter_name[0]

    def extract_chapter_name(self, extracted_page, chapter_name):
        """Remove chapter name from page text."""
        extracted_page.text = extracted_page.text.lstrip(chapter_name)


class Splitter:
    def _find_first_match(self, patterns, content_text):
        """Return first regex match across patterns, or None."""
        for pattern in patterns:
            match = re.search(pattern, content_text)
            if match:
                return match
        return None

    def _extract_sublevel_name(self, patterns, content_text):
        match = self._find_first_match(patterns, content_text)
        if match:
            return re.sub(match.re.pattern, "", content_text)
        WarnAndExit("Unable to extract chapter name.")

    def _holds_new_sublevels(self, patterns, content_text):
        return self._find_first_match(patterns, content_text) is not None

    def _split_on_single_pattern(self, pattern, content_text, remove_separator=False):
        resulting_parts = re.split(pattern, content_text)
        if resulting_parts[0] == "":
            # As stated in the documentation of the re package:
            #    If there are capturing groups in the separator and it
            #    matches at the start of the string, the result will start
            #    with an empty string.
            # In which case we thus have to remove the heading empty string.
            del resulting_parts[0]
            # When the breaking pattern occurs at the very beginning of the
            # string, the re.split() list will start with an empty string which
            # was taken care of in the above line. But in this case, the empty
            # string is also followed by the encountered separator. When
            # looking for paragraphs the separator carries no information
            # (there is no equivalent of chapter name) and we can remove it
            # here:
            if remove_separator:
                del resulting_parts[0]  # Above deletion made indexes change
            # As stated in the documentation of the re package, and concerning
            # a match of the separator:
            #    The same holds for the end of the string.
            # (that is the result will end with an empty string)
        if resulting_parts[-1] == "":
            del resulting_parts[-1]
        if resulting_parts[-1] == "\n":
            del resulting_parts[-1]
        return resulting_parts

    def _split(self, patterns, content_text):
        if not self._holds_new_sublevels(patterns, content_text):
            Warning("split() was called when there was nothing to split.")
            # Wrap the input in a list because the caller expects the
            # returned value to be the result of re.split() (that is a
            # list())
            return [content_text]
        if len(patterns) > 2:
            # Things were simply not tested with more than two patterns...
            WarnAndExit("Capturing groups ambiguity with too many patterns")
        # As stated in the documentation of the re package:
        #    If capturing parentheses are used in pattern, then the text of
        #    all groups in the pattern are also returned as part of the
        #    resulting list.
        first_parts = self._split_on_single_pattern(
            r"(" + patterns[0] + r")", content_text
        )

        resulting_parts = []
        for part_text in first_parts:
            resulting_parts += self._split_on_single_pattern(
                r"(" + patterns[1] + r")", part_text
            )
        if resulting_parts[-1] == "\n":
            del resulting_parts[-1]
        return resulting_parts

    def _get_sublevel_name(
        self, sublevel_patterns, name_extraction_pattern, content_text
    ):
        match = self._find_first_match(sublevel_patterns, content_text)
        if match:
            # Deal with the multiline case
            sublevel_name = re.search(name_extraction_pattern, match.group(0)).group(0)
            return re.sub("\n", " ", sublevel_name)
        Warning("Sublevel name not found.")
        return None


class SinglePatternSplitter(Splitter):
    """A splitter using a single pattern to detect the breaking zone. A second sub-pattern is used to extract the name of the document structural element."""

    def __init__(self, breaking_pattern, name_pattern):
        self.breaking_pattern = breaking_pattern
        self.name_pattern = name_pattern

    def holds_new_sublevels(self, content_text):
        return Splitter._holds_new_sublevels(
            self, [self.breaking_pattern], content_text
        )

    def split(self, content_text):
        # As stated in the documentation of the re package:
        #    If capturing parentheses are used in pattern, then the text of
        #    all groups in the pattern are also returned as part of the
        #    resulting list.
        return Splitter._split_on_single_pattern(
            self, r"(" + self.breaking_pattern + r")", content_text
        )

    def get_sublevel_name(self, content_text):
        return Splitter._get_sublevel_name(
            self,
            [self.breaking_pattern],
            self.name_pattern,
            content_text,
        )


class MultiplePatternSplitter(Splitter):
    """A splitter using a list of possible patterns to detect the breaking zone. A second sub-pattern is used to extract the name of the document structural element."""

    def __init__(self, breaking_patterns, name_pattern):
        self.breaking_patterns = breaking_patterns
        self.name_pattern = name_pattern

    def holds_new_sublevels(self, content_text):
        return Splitter._holds_new_sublevels(self, self.breaking_patterns, content_text)

    def split(self, content_text):
        return Splitter._split(self, self.breaking_patterns, content_text)

    def get_sublevel_name(self, content_text):
        return Splitter._get_sublevel_name(
            self,
            self.breaking_patterns,
            self.name_pattern,
            content_text,
        )

    def extract_sublevel_name(self, content_text):
        return Splitter._extract_sublevel_name(
            self,
            self.breaking_patterns,
            content_text,
        )


class NameLessSinglePatternSplitter(SinglePatternSplitter):
    """When breaking paragraphs into sentences there is no need to extract a name for the Sentence structural element."""

    def __init__(self, breaking_pattern):
        SinglePatternSplitter.__init__(self, breaking_pattern, "dummy_pattern")

    def split(self, content_text):
        return Splitter._split_on_single_pattern(
            self, self.breaking_pattern, content_text, remove_separator=True
        )

    def get_sublevel_name(self, dummy_content_text):
        return None

    def extract_sublevel_name(self, dummy_content_text):
        return
