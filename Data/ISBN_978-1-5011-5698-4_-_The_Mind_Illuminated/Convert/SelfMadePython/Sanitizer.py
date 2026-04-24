import re


class Sanitizer:
    """Sanitizer for The Mind Illuminated book."""

    def __init__(self):
        self.figure_separator = r"((?:\n)+Figure)"

    def sanitize_page_text(self, extracted_page):
        """
        After extraction of the text from the original pdf, some ad hoc
        manual cleaning is alas required.
        """
        figure_matches = re.findall(self.figure_separator, extracted_page.text)
        if figure_matches:
            extracted_page.text = re.sub(
                self.figure_separator,
                "\nFigure <<Converter note: picture removed>>",
                extracted_page.text,
            )
