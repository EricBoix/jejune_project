import sys

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

    def _initialize_chapter_page(self):
        if bool(self._chapter_page):
            # Already initialized
            return
        current_chapter_page = None
        for page_number in range(0, self.total_page_number):
            if self._is_chapter_beginning_page(page_number):
                current_chapter_page = page_number
            self._chapter_page[page_number] = current_chapter_page

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
        self._initialize_chapter_page()
        return self._chapter_page[page_number]

    def _get_chapter_page(self, page_number):
        chapter_page_number = self._get_chapter_page_number(page_number)
        return self.pages_info[chapter_page_number]

    def _get_chapter_info(self, page_number):
        chapter_page = self._get_chapter_page(page_number)
        if not "chapter_info" in chapter_page:
            print("Chapter page without chapter_info (page number ", page_number, ").")
            print("Exiting")
            sys.exit()
        return chapter_page["chapter_info"]

    def _get_chapter_name(self, page_number):
        chapter_info = self._get_chapter_info(page_number)
        if not "name" in chapter_info:
            print(
                "chapter_info of chapter page (page number ",
                page_number,
                ") without name.",
            )
            print("Exiting")
            sys.exit()
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
