import re


class TextSanitizer:
    """Text sanitization utilities for extracted PDF content."""

    def sanitize_newlines_and_multiple_whitespaces(self, input_text: str) -> str:
        """Remove newlines and collapse multiple whitespaces.

        Newlines are encountered to denote different usages:
        - set some tabulations of illuminations (example "\\       ")
        - define a new paragraph in which case newline is followed by
          exactly 4 whitespaces (example "\\n    "): refer to
          break_chapter_into_paragraphs() method
        - simple line folding within original paragraphs or even sentences
          where newlines are used to format the original pdf with line returns.
        """
        input_text = input_text.replace("\n", " ")
        return re.sub(r"\s+", " ", input_text).strip()
