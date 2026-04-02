import sys
import re
from ConvertPdfToMarkdown import ExtractedPageBase


class ExtractedPage(ExtractedPageBase):

    def __init__(self, page_number, layout, original_page):
        ExtractedPageBase.__init__(self, page_number, layout, original_page)
        self.chapter_name_separator_regex = r"((?:\n){3,}(\w| ))"
        self.chapter_name_separator_first_occurrence = 100
        self.figure_separator = r"((?:\n)+Figure)"

        try:
            original_page_text = self.original_pdf_page.extract_text(
                extraction_mode="layout"
            )
        except NotImplementedError:
            # Fallback for PDFs with filter arrays that pypdf can't handle
            # in layout mode
            original_page_text = self.original_pdf_page.extract_text()

        # For some undocumented reason pdfreader output has TAB ("\t"
        # character) in place of spaces. Brutally convert those tabulations to
        # spaces everywhere:
        original_page_text = re.sub("\\t", " ", original_page_text)

        # Remove the heading bunch of whitespaces (and assimilated characters)
        self.text = original_page_text.lstrip()

    def is_chapter_beginning_page(self):
        match = re.search(self.chapter_name_separator_regex, self.text)
        if not match:
            return False
        if match.start() > self.chapter_name_separator_first_occurrence:
            # The separator has to be encountered quite early in the page.
            # This is quite artificial and done to weed out odd occurrences...
            return False
        return True

    def get_chapter_name(self):
        chapter_name = re.split(self.chapter_name_separator_regex, self.text)
        if not chapter_name:
            print(
                "Chapter name ",
                chapter_name,
                " not found in extracted page ",
                self.text,
            )
            print("Exiting")
            sys.exit()
        return chapter_name[0]

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
