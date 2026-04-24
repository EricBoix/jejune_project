import re
from typing import Optional

import roman

from ConvertPdfToMarkdown import StructuralInfoBase, Splitter, WarnAndExit


class StructuralInfo(StructuralInfoBase):
    # The structural information per se with extension specifics
    # - "type" can be "illustration" (with an optional "header" boolean flag)
    # - a "chapter_info" can have an optional "illumination_delimiter"

    class chapter_splitter:
        """Chapter splitter for Collecting Gold Dust.

        Detects chapter boundaries based on:
        1. Static declarations in pages_info (type == "chapter")
        2. Exactly 6 newlines
        """

        def __init__(self, structural_info):
            self.structural_info = structural_info
            # The following regex stands for
            # (?<!(\n)): negative lookbehind for a newline (that is: make sure
            #            we start the match at the first newline occurrence)
            # (\n){6}: match six newlines (note: but they can be more than that
            #          standing afterwards. Hence, if we where to leave the
            #          regex like that, it could be that they are more newlines
            #          than 6.)
            # (?!(\n)): look-forward stating that when matching the above 6
            #          newlines the next character can NOT be a newline.
            # The whole regex thus states: match EXACTLY (no more, no less) 6
            # newlines.
            self.chapter_name_separator_regex = r"(?<!(\n))(\n){6}(?!(\n))"
            self.chapter_name_separator_first_occurrence = 100

        def holds_new_chapter(self, extracted_page) -> bool:
            # First check static declaration in pages_info
            if self.structural_info._holds_new_chapter(extracted_page.page_number):
                return True
            # Then check regex pattern
            match = re.search(self.chapter_name_separator_regex, extracted_page.text)
            if not match:
                return False
            if match.start() > self.chapter_name_separator_first_occurrence:
                return False
            return True

        def get_chapter_name(self, extracted_page) -> Optional[str]:
            # First check static declaration in pages_info
            if self.structural_info._holds_new_chapter(extracted_page.page_number):
                return self.structural_info._get_chapter_name(
                    extracted_page.page_number
                )
            # Then use regex extraction
            chapter_name = re.split(
                self.chapter_name_separator_regex, extracted_page.text
            )
            if not chapter_name:
                WarnAndExit(
                    f"Chapter name {chapter_name} not found in extracted page {extracted_page.text}"
                )
            return chapter_name[0]

        def extract_chapter_name(self, extracted_page, chapter_name):
            """Remove chapter name from page text."""
            extracted_page.text = extracted_page.text.lstrip(chapter_name)

    class superchapter_to_chapter_splitter(Splitter):
        def __init__(self):
            # Sub-chapters typically start with e.g.
            #    "\n\n\nUSING WISDOM\n.
            # We thus need to define three parts for the pattern
            # 1. the ante chapter breaking lines
            self.chapter_name_ante_pattern = r"\n\n\n"
            # 2. the name of the chapter per se. Note that the minimum number
            # for matching has to be
            # - at least 2 in order not to match the first (capital letter of
            #   a sentence) e.g. "Stand by me."
            # - at least three not to match e.g. "A cat was run over." where the
            #   the initial capital and its following whitespace would match.
            # For the upper limit to, well a full line should suffice.
            self.chapter_name_pattern = r"[A-Z|?|\”|\“|,| ]{3,100}"
            # 3. the trailing return
            self.chapter_name_post_pattern = r"\n"

            self.breaking_pattern = (
                self.chapter_name_ante_pattern
                + self.chapter_name_pattern
                + self.chapter_name_post_pattern
            )

        def holds_new_sublevels(self, content_text):
            return Splitter._holds_new_sublevels(
                self, [self.breaking_pattern], content_text
            )

        def split(self, content_text):
            # As stated in the documentation of the re package:
            #    If capturing parentheses are used in pattern, then the text of
            #    all groups in the pattern are also returned as part of the
            #    resulting list.
            return Splitter._split_on_single_pattern(
                self, r"(" + self.breaking_pattern + r")", content_text
            )

        def get_sublevel_name(self, content_text):
            return Splitter._get_sublevel_name(
                self,
                [self.breaking_pattern],
                self.chapter_name_pattern,
                content_text,
            )

        def extract_sublevel_name(self, content_text):
            return Splitter._extract_sublevel_name(
                self,
                [self.breaking_pattern],
                content_text,
            )

    class chapter_to_paragraph_splitter:
        def __init__(self):
            self.breaking_pattern = "\n    "

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

    @property
    def total_page_number(self) -> int:
        return 160

    def __init__(self):
        StructuralInfoBase.__init__(self)
        # The original pdf document has a title that is depicted (as opposed to
        # written in text) in the cover illustration and thus cannot be
        # automatically extracted. This title ends-up embedded in some headers
        # and must thus be manually provided.
        self.book_title = "COLLECTING GOLD DUST: Nurturing the Dhamma in Daily Living"

        # The preamble section pages use roman numbering. This offsets the
        # numbering of the body pages
        self.page_numbering_offset = 16

        self._pages_info = {
            0: {"drop_page": True},  # Front cover
            1: {"drop_page": True},  # Book title
            2: {"drop_page": True},  # Illustration
            3: {
                # Chapters with no given name are artificial/fake chapters that
                # do not exist in the book. They are a technicality for the
                # first pages not to be devoid of a belonging chapter:
                "type": "chapter",
                "chapter_info": {
                    "name": "Introduction (ghost chapter)",
                    "illumination_delimiter": None,
                },
            },
            4: {"drop_page": True},
            5: {
                # They are two reasons for which we don't have to look for
                # a paragraph continuation on the next page:
                # 1. because the page ends a chapter (and hence the paragraph
                #    has to be finished)
                # 2. It just so happens that the paragraph ends up nicely at
                #    the bottom of this page.
                # Here we encountered the first case
                "paragraph_fits_on_page": True,
            },
            # 6: implicit "generic"/default page
            7: {
                "chapter_info": {"illumination_delimiter": "MBhaddanta"},
                "paragraph_fits_on_page": True,  # This page ends the chapter
            },
            9: {"chapter_info": {"illumination_delimiter": "Iobservation"}},
            15: {"chapter_info": {"illumination_delimiter": "Wwords"}},
            16: {"paragraph_fits_on_page": True},  # This page ends the chapter
            17: {"drop_page": True},
            18: {"drop_page": True},
            19: {"drop_page": True},
            20: {
                # Although this illustration is decorated with text (or the other way round), the text content is an extracted quote
                # from the body of the chapter. We can thus drop it without
                # content loss.
                "drop_page": True,
            },
            21: {"chapter_info": {"illumination_delimiter": "Ytime"}},
            24: {"drop_page": True},  # Illustration with non meaningful text
            30: {"drop_page": True},  # Illustration with non meaningful text
            35: {"paragraph_fits_on_page": True},  # Paragraph nicely ended.
            36: {"drop_page": True},  # Illustration with non meaningful text
            37: {"paragraph_fits_on_page": True},
            39: {"paragraph_fits_on_page": True},
            41: {"paragraph_fits_on_page": True},  # This page ends the chapter
            42: {
                # This illustration has some additional textual content that
                # is original and that is not part of the main text.
                # We thus keep it.
                "type": "illustration",
            },
            43: {"chapter_info": {"illumination_delimiter": "WTwo"}},
            44: {"drop_page": True},  # Illustration with non meaningful text
            45: {"paragraph_fits_on_page": True},
            46: {"paragraph_fits_on_page": True},
            48: {"paragraph_fits_on_page": True},
            50: {"drop_page": True},  # Illustration with non meaningful text
            51: {"paragraph_fits_on_page": True},
            53: {"paragraph_fits_on_page": True},
            56: {"drop_page": True},  # Illustration with non meaningful text
            60: {"paragraph_fits_on_page": True},
            62: {"drop_page": True},  # Illustration with non meaningful text
            63: {"paragraph_fits_on_page": True},
            64: {"type": "illustration"},  # Illustration with valid text
            65: {"chapter_info": {"illumination_delimiter": "Man"}},
            67: {"paragraph_fits_on_page": True},
            68: {"drop_page": True},
            70: {"paragraph_fits_on_page": True},
            72: {"paragraph_fits_on_page": True},
            73: {"paragraph_fits_on_page": True},
            74: {"drop_page": True},
            76: {"paragraph_fits_on_page": True},
            77: {"drop_page": True},
            78: {"type": "illustration"},
            79: {"chapter_info": {"illumination_delimiter": "Dnot"}},
            80: {"paragraph_fits_on_page": True},
            82: {"drop_page": True},
            84: {"paragraph_fits_on_page": True},
            87: {"paragraph_fits_on_page": True},
            88: {"drop_page": True},
            89: {"paragraph_fits_on_page": True},
            90: {"type": "illustration"},
            91: {"chapter_info": {"illumination_delimiter": "Wchange"}},
            92: {"paragraph_fits_on_page": True},
            94: {"drop_page": True},
            96: {"paragraph_fits_on_page": True},
            98: {"paragraph_fits_on_page": True},
            99: {"paragraph_fits_on_page": True},
            100: {"drop_page": True},
            # 101: dalmatians
            102: {"paragraph_fits_on_page": True},
            106: {"drop_page": True},
            111: {"paragraph_fits_on_page": True},
            112: {"drop_page": True},
            114: {"paragraph_fits_on_page": True},
            117: {"paragraph_fits_on_page": True},
            118: {"drop_page": True},
            119: {"paragraph_fits_on_page": True},
            123: {"paragraph_fits_on_page": True},
            124: {"type": "illustration"},
            125: {
                "chapter_info": {"illumination_delimiter": "Wawareness"},
                "paragraph_fits_on_page": True,
            },
            128: {"type": "illustration"},
            132: {"paragraph_fits_on_page": True},
            133: {
                "type": "illustration",
                # By default illustrations have no header, unless ... they do
                "header": True,
            },
            134: {"type": "illustration"},
            135: {
                # In order to remove this chapter definition, one needs to
                # deal with patterning distinction between chapter and
                # sub-chapter
                "type": "chapter",
                "chapter_info": {
                    "name": "Continuing the Work",
                    "illumination_delimiter": "A remember",
                },
            },
            136: {"paragraph_fits_on_page": True},
            137: {"paragraph_fits_on_page": True},
            138: {"type": "illustration"},
            143: {"paragraph_fits_on_page": True},
            144: {"type": "illustration"},
            145: {"chapter_info": {"illumination_delimiter": "Sour"}},
            147: {"paragraph_fits_on_page": True},
            148: {"paragraph_fits_on_page": True},
            149: {"paragraph_fits_on_page": True},
            150: {"type": "illustration"},
            152: {"paragraph_fits_on_page": True},
            153: {"paragraph_fits_on_page": True},
            154: {"paragraph_fits_on_page": True},
            156: {"type": "illustration"},
            157: {"paragraph_fits_on_page": True},
            158: {
                "type": "chapter",
                "chapter_info": {
                    "name": "Dedication",
                    "illumination_delimiter": None,
                },
                "paragraph_fits_on_page": True,
            },
            159: {"type": "illustration"},  # This Back cover of the book
        }

    @property
    def pages_info(self) -> dict:
        return self._pages_info

    def convert_to_logical_page_number(self, page_number):
        if page_number == 0:
            return "Cover"
        # Deal with the first pages numbering that uses roman numeration
        if page_number >= 1 and page_number <= self.page_numbering_offset + 1:
            return roman.toRoman(page_number).lower()
        else:
            return str(page_number - self.page_numbering_offset)

    def _page_is_illustration(self, page_number):
        if not page_number in self.pages_info:
            return False
        if not "type" in self.pages_info[page_number]:
            return False
        if self.pages_info[page_number]["type"] == "illustration":
            return True
        return False

    ##### Header related thingies

    def _page_is_headless(self, page_number):
        # Only illustrations can be headless
        if not self._page_is_illustration(page_number):
            return False
        # Yet some illustrations still have a header
        if "header" in self.pages_info[page_number]:
            return False
        # Eventually illustrations not flagged as having a header are headless
        return True

    def _page_is_skipped(self, page_number):
        return self._page_is_illustration(page_number) or self._page_is_dropped(
            page_number
        )

    def book_title_page_header(self, page_number):
        return (
            self.convert_to_logical_page_number(page_number)
            + r" \| "
            + self.book_title
        )
