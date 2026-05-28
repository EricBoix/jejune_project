import roman

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
        """Chapter splitter for Collecting Gold Dust.

        Detects chapter boundaries based on:
        1. Static declarations in pages_info (type == "chapter")
        2. Exactly 6 newlines
        """

        def __init__(self, structural_info):
            structural_info = structural_info
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
            chapter_name_separator_regex = r"(?<!(\n))(\n){6}(?!(\n))"
            chapter_name_separator_first_occurrence = 100
            ChapterSplitter.__init__(
                self,
                structural_info,
                chapter_name_separator_regex,
                chapter_name_separator_regex,  # Extractor = Separator
                chapter_name_separator_first_occurrence,
            )

    # class superchapter_to_chapter_splitter(SinglePatternSplitter):
    class superchapter_to_chapter_splitter(MultiplePatternSplitter):
        def __init__(self):
            # Refer to comments of test class TestChapterRegex within
            # test_main.py for explanations
            chapter_name_characters = r"[A-Z|?|’| \u201c\u201d,]{3,100}"
            multi_lines_chapter_name = (
                r"(?:"
                + chapter_name_characters
                + r"\n(?! ))*"
                + chapter_name_characters
            )
            middle_page_subchapter_pattern = (
                r"\n\n\n" + multi_lines_chapter_name + r"\n"
            )
            top_page_subchapter_pattern = r"^" + multi_lines_chapter_name
            breaking_patterns = [  # Visual sugar
                middle_page_subchapter_pattern,
                top_page_subchapter_pattern,
            ]
            MultiplePatternSplitter.__init__(
                self,
                breaking_patterns,
                multi_lines_chapter_name,
            )

    class chapter_to_paragraph_splitter(NameLessSinglePatternSplitter):
        def __init__(self):
            breaking_pattern = "\n    "
            NameLessSinglePatternSplitter.__init__(self, breaking_pattern)

    @property
    def total_page_number(self) -> int:
        return 160

    def __init__(self):
        StructuralInfoBase.__init__(self)
        self._sanitizer = None
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
            self.convert_to_logical_page_number(page_number) + r" \| " + self.book_title
        )

    def set_page_header_callback(self, get_page_header):
        """Set the page header callback and create the sanitizer."""
        self._sanitizer = Sanitizer(self, get_page_header)

    def sanitize_page_text(self, extracted_page):
        self._sanitizer.sanitize_page_text(extracted_page)
