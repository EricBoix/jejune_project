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
        # belongs to. In other terms for this dictionary
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

    def _get_chapter_page(self, page_number):
        self._initialize_chapter_page()
        return self._chapter_page[page_number]

    def _get_chapter_name(self, page_number):
        chapter_page = self._get_chapter_page(page_number)
        return self.pages_info[chapter_page]["chapter_info"]["name"]

    def _is_chapter_beginning_page(self, page_number):
        if not page_number in self.pages_info:
            return False
        if not "type" in self.pages_info[page_number]:
            return False
        if self.pages_info[page_number]["type"] == "chapter":
            return True
        return False
