import re
from .Warning import Warning, WarnAndExit


class Splitter:
    def _extract_sublevel_name(self, patterns, content_text):
        for pattern in patterns:
            match = re.search(pattern, content_text)
            if match:
                return re.sub(pattern, "", content_text)
        WarnAndExit("Unable to extract chapter name.")

    def _holds_new_sublevels(self, patterns, content_text):
        for pattern in patterns:
            match = re.search(pattern, content_text)
            if match:
                return True
        return False

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
            WarnAndExit("Capturing groups ambiguity with too many patterns")
        # As stated in the documentation of the re package:
        #    If capturing parentheses are used in pattern, then the text of
        #    all groups in the pattern are also returned as part of the
        #    resulting list.
        first_parts = self._split_on_single_pattern(
            r"(" + patterns[0] + r")", content_text
        )
        # Notice that in the second pattern is not transformed to become
        # a capturing group ( that is placed into parentheses( + pattern +)).
        # Otherwise trouble happens with extra None thrown into the list.
        # Things where not tested with more than two patterns...
        resulting_parts = []
        for part_text in first_parts:
            resulting_parts += self._split_on_single_pattern(patterns[1], part_text)
        if resulting_parts[-1] == "\n":
            del resulting_parts[-1]
        return resulting_parts

    def _get_sublevel_name(
        self, sublevel_patterns, name_extraction_pattern, content_text
    ):
        for pattern in sublevel_patterns:
            # Note: the following re.search is exactly the one encountered
            # in Splitter._holds_new_sublevels(), which somehow bypasses the
            # DRY (Don't Repeat Yourself) principle
            match = re.search(pattern, content_text)
            if match:
                return re.search(
                    name_extraction_pattern,
                    match.group(0),
                ).group(0)
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
