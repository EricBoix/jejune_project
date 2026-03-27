import re
from .Warning import Warning, WarnAndExit

# The structural information constituted by the presence of chapters,
# illustrations, illumination, headers ... is quite often difficult
# to be automatically discovered. While waiting for better (and free)
# tools, the following was manually extracted and summarized in the
# following dictionary.


class StructuralInfoBase:
    # Derived classes commit to have a pages_info dictionary of the form
    #
    # self.pages_info = {
    #    0: {                                # 0 stands for the page number
    #       "type": "chapter",
    #       "chapter_info": {                  # Additional info for chapters
    #          "name": "Preamble",
    #          "illumination_delimiter": None,
    #       },
    #    },
    #    1: {
    #       "type": "generic",
    #       "drop_page": True,             # Optional flag to drop content
    #    },
    # }
    #
    # Derived classes can extend the available type, that by default are
    # restricted to be among.  {"chapter", "generic"}

    def __init__(self):
        # Technical (optimisation) variable used to hold the correspondance
        # between a given page number and the chapter to which that page
        # belongs to. In other terms, within this dictionary
        #  - a key is a page number
        #  - the associated value holds the current chapter number for that key
        self._chapter_page = {}

    def set_chapter_page_number(self, page_number: int, chapter_page_number: int):
        """Set the chapter page number of the page designated by page number.

        :param int page_number: The page number of the page for which we are setting the chapter (page)
        :param int chapter_page_number The page number of the chapter (beginning) to which the designated belongs to.
        """
        if page_number in self._chapter_page:
            WarnAndExit(
                f"Trying to overwrite chapter page of page number {page_number}."
            )
        self._chapter_page[page_number] = chapter_page_number

    def _page_is_dropped(self, page_number):
        if not page_number in self.pages_info:
            return False
        if not "drop_page" in self.pages_info[page_number]:
            return False
        return True

    def _page_is_skipped(self, page_number):
        """
        The derived classes might overload this definition with their specific considerations.
        """
        return self._page_is_dropped(page_number)

    def _get_chapter_page_number(self, page_number):
        if page_number not in self._chapter_page:
            WarnAndExit(f"Unknown chapter page of page number {page_number}.")
        return self._chapter_page[page_number]

    def _get_chapter_page(self, page_number):
        chapter_page_number = self._get_chapter_page_number(page_number)
        return self.pages_info[chapter_page_number]

    def _get_chapter_info(self, page_number):
        chapter_page = self._get_chapter_page(page_number)
        if not "chapter_info" in chapter_page:
            WarnAndExit(
                f"Chapter page without chapter_info (page number {page_number})."
            )
        return chapter_page["chapter_info"]

    def _get_chapter_name(self, page_number):
        chapter_info = self._get_chapter_info(page_number)
        if not "name" in chapter_info:
            Warning(
                f"chapter_info of chapter page (page number {page_number}) without name.",
            )
            return None
        return chapter_info["name"]

    def _is_chapter_beginning_page(self, page_number):
        if not page_number in self.pages_info:
            return False
        if not "type" in self.pages_info[page_number]:
            return False
        if self.pages_info[page_number]["type"] == "chapter":
            return True
        return False

    def _get_page_number_finishing_last_paragraph(self, page_number):
        """
        A page that is followed by one (or many) skipped pages will need to skip such pages in order to retrieve the end of its last paragraph.
        Return the page number of the first page that holds the content of the end of the paragraph.
        """
        next_page_number = page_number + 1
        while self._page_is_skipped(next_page_number):
            next_page_number += 1
        return next_page_number


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
