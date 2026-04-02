import re
from ConvertPdfToMarkdown import StructuralInfoBase, WarnAndExit, Splitter


class StructuralInfo(StructuralInfoBase):
    # The structural information per se with extension specifics
    # - "type" can be "illustration" (with an optional "header" boolean flag)
    # - a "chapter_info" can have an optional "illumination_delimiter"

    class superchapter_to_chapter_splitter(Splitter):
        def __init__(self):
            # Sub-chapters typically start with e.g.
            #    "85. Time to Die\n\n".
            # We thus need to define three parts for the pattern
            # 1. the chapter number (refer to the peculiarities section of the
            #    Readme.md for an explanation on which there can be one or no
            #    occurrence of the whitespace character)
            self.chapter_number_pattern = r"\d+\.[ ]?"
            # 2. the name of the chapter per se
            self.chapter_name_pattern = r"[A-Za-z-’|?|!|,| ]+"
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
            # Technical variables:
            self.breaking_patterns = [
                self.breaking_pattern_one,
                self.breaking_pattern_two,
            ]

        def holds_new_sublevels(self, content_text):
            return Splitter._holds_new_sublevels(
                self, self.breaking_patterns, content_text
            )

        def split(self, content_text):
            return Splitter._split(self, self.breaking_patterns, content_text)

        def get_sublevel_name(self, content_text):
            return Splitter._get_sublevel_name(
                self,
                self.breaking_patterns,
                self.chapter_number_pattern + self.chapter_name_pattern,
                content_text,
            )

        def extract_sublevel_name(self, content_text):
            return Splitter._extract_sublevel_name(
                self,
                self.breaking_patterns,
                content_text,
            )

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
            return Splitter._holds_new_sublevels(
                self,
                [self.breaking_pattern],
                content_text,
            )

        def split(self, content_text):
            return Splitter._split_on_single_pattern(
                self, self.breaking_pattern, content_text, remove_separator=True
            )

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
                "typo_and_fix": {
                    "typo": "Centreing",
                    "fix": "Centering",
                },
            },
            10: {"paragraph_fits_on_page": True},
            14: {
                "typo_and_fix": {
                    # Yes there is a lot of extra whitespaces in the original
                    "typo": "Sometimes    when    becomes",
                    "fix": "Sometimes when he becomes",
                },
            },
            15: {
                "typo_and_fix": {
                    "typo": "utterly ashamed",
                    "fix": "utterly ashamed.",
                },
            },
            45: {"drop_page": True},  # Empty page
            67: {"drop_page": True},  # Empty page
            87: {"drop_page": True},  # Empty page
            125: {"paragraph_fits_on_page": True},
            181: {"paragraph_fits_on_page": True},
            182: {"paragraph_fits_on_page": True},
            195: {"paragraph_fits_on_page": True},
            201: {"paragraph_fits_on_page": True},
            203: {
                "paragraph_fits_on_page": True,
                "typo_and_fix": {
                    "typo": "sound a-u-m without any a or m",
                    "fix": "sound a-u-m without any a or m.",
                },
            },
            207: {
                "type": "chapter",
                "chapter_info": {
                    "name": "What Is Zen?",
                },
            },
        }

    def convert_to_logical_page_number(self, page_number):
        return page_number
