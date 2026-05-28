import re
from pdf_to_markdown import (
    ChapterSplitter,
    MultiplePatternSplitter,
    NameLessSinglePatternSplitter,
    StructuralInfoBase,
)
from Sanitizer import Sanitizer


class StructuralInfo(StructuralInfoBase):
    # The structural information per se with extension specifics
    # - "type" can be "illustration" (with an optional "header" boolean flag)
    # - a "chapter_info" can have an optional "illumination_delimiter"

    class chapter_splitter(ChapterSplitter):
        """Chapter splitter for Zen Flesh, Zen Bones.

        Detects chapter boundaries based on:
        1. Static declarations in pages_info (type == "chapter")
        2. Pattern matching the chapter title followed by the distributor name
        """

        def __init__(self, structural_info):
            self.distributor_name_pattern = r"OceanofPDF[.]com"
            # Three whitespaces (more or less)
            chapter_name_extractor_regex = r"(\n){3}"
            # The pattern that should match a chapter title definition
            chapter_name_separator_regex = (
                # a bunch of capital letters, or digits with possible white
                # spaces and/or returns
                r"[A-Z\d (\n)]+"
                # _exactly_ three returns,
                + r"(?<!(\n))"
                + chapter_name_extractor_regex
                + r"(?!(\n))"
                # at least 8 white spaces,
                + r"( *){8}"
                # a specific string (refer above)
                + self.distributor_name_pattern
            )
            # The maximum number of characters within an extracted page to look
            # for a chapter title:
            chapter_name_separator_first_occurrence = 100
            ChapterSplitter.__init__(
                self,
                structural_info,
                chapter_name_separator_regex,
                chapter_name_extractor_regex,
                chapter_name_separator_first_occurrence,
            )

        def extract_chapter_name(self, extracted_page, chapter_name):
            """Remove chapter name from page text."""
            # If distributor pattern not in text, use simple removal
            if re.search(self.distributor_name_pattern, extracted_page.text) is None:
                ChapterSplitter.extract_chapter_name(self, extracted_page, chapter_name)
                return
            # For regex-detected chapters (with distributor pattern), remove
            # the full pattern
            extracted_page.text = re.sub(self.separator_regex, "", extracted_page.text)

    class superchapter_to_chapter_splitter(MultiplePatternSplitter):
        def __init__(self):
            # Sub-chapters typically start with e.g.
            #    "85. Time to Die\n\n".
            # We thus need to define three parts for the pattern
            # 1. the chapter number (refer to the peculiarities section of the
            #    Readme.md for an explanation on which there can be one or no
            #    occurrence of the whitespace character)
            chapter_number_pattern = r"\d+\.[ ]?"
            # 2. the name of the chapter per se
            chapter_name_pattern = r"[A-Za-z-’|?|!|,| ]+"
            # 3. the two trailing return
            chapter_name_trailing_returns = r"\n\n"

            breaking_pattern_one = (
                chapter_number_pattern
                + chapter_name_pattern
                + chapter_name_trailing_returns
            )
            # The above pattern works and the chapter name that matches can be
            # safely extracted when this chapter appears at the head of a page.
            # But when the chapter happens in the middle of the page then
            # they are three \n in sequence to separate the chapters. A
            # typical mid-page chapter page is thus e.g.
            #              "\n\n\n86. The Living Buddha and the Tubmaker\n\n"
            # The pattern thus becomes r"(\n\n\n)\d+\.[ ][A-Za-z| ]+"
            middle_page_chapter_name_heading_returns = r"\n\n\n"
            breaking_pattern_two = (
                middle_page_chapter_name_heading_returns + breaking_pattern_one
            )
            # Technical variables:
            breaking_patterns = [
                breaking_pattern_one,
                breaking_pattern_two,
            ]
            MultiplePatternSplitter.__init__(
                self,
                breaking_patterns,
                chapter_number_pattern + chapter_name_pattern,
            )

    class chapter_to_paragraph_splitter(NameLessSinglePatternSplitter):
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
            breaking_pattern = r"\n\n" + r"|" + r"\n    "
            NameLessSinglePatternSplitter.__init__(self, breaking_pattern)

    @property
    def total_page_number(self) -> int:
        return 209

    def __init__(self):
        StructuralInfoBase.__init__(self)
        self._sanitizer = Sanitizer(self)
        # FIXME: could the book_title be extracted automatically ?
        self.book_title = "ZEN FLESH, ZEN BONES"

        self._pages_info = {
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

    @property
    def pages_info(self) -> dict:
        return self._pages_info

    def convert_to_logical_page_number(self, page_number):
        return page_number

    def sanitize_page_text(self, extracted_page):
        self._sanitizer.sanitize_page_text(extracted_page)
