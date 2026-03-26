import sys
import re
from ConvertPdfToMarkdown import StructuralInfoBase


class StructuralInfo(StructuralInfoBase):
    # The structural information per se with extension specifics
    # - "type" can be "illustration" (with an optional "header" boolean flag)
    # - a "chapter_info" can have an optional "illumination_delimiter"

    class superchapter_to_chapter_splitter:
        def __init__(self):
            # Sub-chapters typically start with e.g.
            #    "85. Time to Die\n\n".
            # We thus need to define three parts for the pattern
            # 1. the chapter number
            self.chapter_number_pattern = r"\d+\.[ ]"
            # 2. the name of the chapter per se
            self.chapter_name_pattern = r"[A-Za-z| ]+"
            # 3. the two trailing return
            self.chapter_name_trailing_returns = r"\n\n"

            self.breaking_pattern_one = (
                self.chapter_number_pattern
                + self.chapter_name_pattern
                + self.chapter_name_trailing_returns
            )
            # The above pattern works and the chapter name that matches can be
            # safely extracted when this chapter appears at the head of a page.
            # But when the chapter happens in the middle of the page then
            # they are three \n in sequence to separate the chapters. A
            # typical mid-page chapter page is thus e.g.
            #              "\n\n\n86. The Living Buddha and the Tubmaker\n\n"
            # The pattern thus becomes r"(\n\n\n)\d+\.[ ][A-Za-z| ]+"
            self.middle_page_chapter_name_heading_returns = r"\n\n\n"
            self.breaking_pattern_two = (
                self.middle_page_chapter_name_heading_returns
                + self.breaking_pattern_one
            )

        def holds_new_sublevels(self, content_text):
            match = re.search(self.breaking_pattern_one, content_text)
            if match:
                return True
            match = re.search(self.breaking_pattern_two, content_text)
            if match:
                return True
            return False

        def split(self, content_text):
            if not self.holds_new_sublevels(content_text):
                print("Warning: split() was called when there was nothing to split.")
                # Wrap the input in a list because the caller expects the
                # returned value to be the result of re.split()
                return [content_text]

            # As stated in the documentation of the re package:
            #    If capturing parentheses are used in pattern, then the text of
            #    all groups in the pattern are also returned as part of the
            #    resulting list.
            parts_one = re.split(r"(" + self.breaking_pattern_one + r")", content_text)
            if parts_one[0] == "":
                # As stated in the documentation of the re package:
                #    If there are capturing groups in the separator and it
                #    matches at the start of the string, the result will start
                #    with an empty string.
                # In which case we thus have to remove the heading empty string.
                del parts_one[0]
            if parts_one[-1] == "":
                # As stated in the documentation of the re package:
                #    The same holds for the end of the string.
                del parts_one[-1]
            resulting_parts = []
            for parts in parts_one:
                resulting_parts += re.split(self.breaking_pattern_two, parts)
            return resulting_parts

        def get_sublevel_name(self, content_text):
            match = re.search(self.breaking_pattern_one, content_text)
            if match:
                return re.search(
                    self.chapter_number_pattern + self.chapter_name_pattern,
                    match.group(0),
                ).group(0)
            match = re.search(self.breaking_pattern_two, content_text)
            if match:
                name_match = re.search(
                    self.chapter_number_pattern + self.chapter_name_pattern,
                    match.group(0),
                ).group(0)
                return name_match
            print("Warning: sublevel name not found.")
            return None

        def extract_sublevel_name(self, content_text):
            match = re.search(self.breaking_pattern_one, content_text)
            if match:
                return re.sub(self.breaking_pattern_one, "", content_text)
            match = re.search(self.breaking_pattern_two, content_text)
            if match:
                return re.sub(self.breaking_pattern_one, "", content_text)
            print("Unable to extract chapter name.")
            print("Exiting")
            sys.exit()

    class chapter_to_paragraph_splitter:
        def __init__(self):
            # The paragraph termination varies within the document:
            #  - within the Foreword chapter it takes the form of a double
            #    newline character
            #  - but within the "101 Zen Stories" the paragraph termination
            #    takes the form of a newline character followed by three
            #    whitespaces.
            # Deal with both cases. Additionally, notice that we must avoid
            # having two capturing groups: refer to e.g.
            # https://stackoverflow.com/questions/11320231/re-split-with-multiple-arguments-or-returns-none
            # and thus patterns are NOT wrapped in parentheses.
            self.breaking_pattern = r"\n\n" + r"|" + r"\n    "

        def holds_new_sublevels(self, content_text):
            match = re.search(self.breaking_pattern, content_text)
            if match:
                return True
            return False

        def split(self, content_text):
            if not self.holds_new_sublevels(content_text):
                print(
                    "Split() probably shouldn't be called when there is nothing to split."
                )
            result = re.split(self.breaking_pattern, content_text)
            # When the breaking pattern occurs at the very beginning of the
            # string, the re.split() list will start with an empty string
            # followed by the encountered separator. Clean that up:
            if result[0] == "":
                del result[0]
                del result[0]  # Things have changed since the first del ;-)
            return result

        def get_sublevel_name(self, content_text):
            return None

        def extract_sublevel_name(self, content_text):
            return

    def __init__(self):
        StructuralInfoBase.__init__(self)

        self.total_page_number = 209
        # FIXME: could the book_title be extracted automatically ?
        self.book_title = "ZEN FLESH, ZEN BONES"

        self.pages_info = {
            0: {"drop_page": True},  # Front cover
            1: {"drop_page": True},  # Book title
            2: {"drop_page": True},  # Table Of Content (TOC)
            3: {"drop_page": True},  # ...
            4: {"drop_page": True},  # ...
            5: {"drop_page": True},  # ...
            6: {"drop_page": True},  # end of TOC
            7: {
                # Alas the first chapters does not follow the pattern allowing
                # it to be extracted automatically. This is thus a manual
                # override of the default chapter extraction mechanism:
                "type": "chapter",
                "chapter_info": {
                    "name": "Foreword",
                },
            },
            8: {"paragraph_fits_on_page": True},
            9: {"paragraph_fits_on_page": True},
            10: {"paragraph_fits_on_page": True},
            45: {"drop_page": True},  # Empty page
            67: {"drop_page": True},  # Empty page
            87: {"drop_page": True},  # Empty page
            124: {"paragraph_fits_on_page": True},
            194: {"paragraph_fits_on_page": True},
        }

    def convert_to_logical_page_number(self, page_number):
        return page_number
