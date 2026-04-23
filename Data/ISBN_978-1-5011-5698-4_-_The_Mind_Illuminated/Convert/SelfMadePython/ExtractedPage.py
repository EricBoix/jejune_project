import re
from ConvertPdfToMarkdown import ExtractedPageBase


class ExtractedPage(ExtractedPageBase):

    def __init__(self, page_number, layout, original_page):
        ExtractedPageBase.__init__(self, page_number, layout, original_page)
        self.figure_separator = r"((?:\n)+Figure)"

    def sanitize_figures(self):
        # Note: other sources of inspiration concerning regex usage
        #  https://www.daniweb.com/programming/software-development/threads/309017/regex-search-for-longest-set-of-repeating-characters
        figure_matches = re.findall(self.figure_separator, self.text)
        if figure_matches:
            self.text = re.sub(
                self.figure_separator,
                "\nFigure <<Converter note: picture removed>>",
                self.text,
            )
