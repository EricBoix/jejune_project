import sys

from ConvertPdfToMarkdown import StructuralInfoBase

import roman


class StructuralInfo(StructuralInfoBase):
    # The structural information per se with extension specifics
    # - "type" can be "illustration" (with an optional "header" boolean flag)
    # - a "chapter_info" can have an optional "illumination_delimiter"

    def __init__(self):
        StructuralInfoBase.__init__(self)

        self.total_page_number = 160
        # The original pdf document has a title that is depicted (as opposed to
        # written in text) in the cover illustration and thus cannot be
        # automatically extracted. This title ends-up embedded in some headers
        # and this thus a must have.
        self.book_title = "COLLECTING GOLD DUST: Nurturing the Dhamma in Daily Living"
        # Note: the second part of pattern happens on sub-chapter beginnings.
        # Instead of simply starting a new paragraph we should start a new
        # sub-chapter!
        self.chapter_to_paragraph_breaking_pattern = "\n    " + "|" + "\n\n\n"

        # The preamble section pages use roman numbering. This offsets the
        # numbering of the body pages
        self.page_numbering_offset = 16

        self.pages_info = {
            0: {"drop_page": True},  # Front cover
            1: {"drop_page": True},  # Book title
            2: {"drop_page": True},  # Illustration
            3: {
                # Chapters with no given name are artificial/fake chapters that
                # do not exist in the book. They are a technicality for the
                # first pages not to be devoid of belonging chapter:
                "type": "chapter",
                "chapter_info": {"name": "", "illumination_delimiter": None},
            },
            4: {"drop_page": True},
            5: {
                # Another fake/ghost chapter
                "type": "chapter",
                "chapter_info": {"name": "", "illumination_delimiter": None},
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
                "type": "chapter",
                "chapter_info": {
                    "name": "Acknowledgements",
                    "illumination_delimiter": "MBhaddanta",
                },
                "paragraph_fits_on_page": True,  # This page ends the chapter
            },
            9: {
                "type": "chapter",
                "chapter_info": {
                    "name": "Dear Reader",
                    "illumination_delimiter": "Iobservation",
                },
            },
            15: {
                "type": "chapter",
                "chapter_info": {
                    "name": "On Language",
                    "illumination_delimiter": "Wwords",
                },
            },
            16: {"paragraph_fits_on_page": True},  # This page ends the chapter
            17: {"drop_page": True},
            18: {"drop_page": True},
            19: {"drop_page": True},
            20: {
                # Although this illustration is decorated with text (or the other way round), the text content text is an extracted quote
                # from the body of the chapter. We can thus drop it without
                # content loss.
                "drop_page": True,
            },
            21: {
                "type": "chapter",
                "chapter_info": {
                    "name": "A Note from the Teacher",
                    "illumination_delimiter": "Ytime",
                },
            },
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
            43: {
                "type": "chapter",
                "chapter_info": {
                    "name": "Mindfulness is a Lifestyle Change",
                    "illumination_delimiter": "WTwo",
                },
            },
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
            65: {
                "type": "chapter",
                "chapter_info": {
                    "name": "Take a Closer Look",
                    "illumination_delimiter": "Man",
                },
            },
            67: {"paragraph_fits_on_page": True},
            68: {"drop_page": True},
            70: {"paragraph_fits_on_page": True},
            72: {"paragraph_fits_on_page": True},
            73: {"paragraph_fits_on_page": True},
            74: {"drop_page": True},
            76: {"paragraph_fits_on_page": True},
            77: {"drop_page": True},
            78: {"type": "illustration"},
            79: {
                "type": "chapter",
                "chapter_info": {
                    "name": "Reflect. Learn. Keep Going.",
                    "illumination_delimiter": "Dnot",
                },
            },
            80: {"paragraph_fits_on_page": True},
            82: {"drop_page": True},
            84: {"paragraph_fits_on_page": True},
            87: {"paragraph_fits_on_page": True},
            88: {"drop_page": True},
            89: {"paragraph_fits_on_page": True},
            90: {"type": "illustration"},
            91: {
                "type": "chapter",
                "chapter_info": {
                    "name": "Day-to-Day",
                    "illumination_delimiter": "Wchange",
                },
            },
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
                "type": "chapter",
                "chapter_info": {
                    "name": "A Lighter Approach",
                    "illumination_delimiter": "Wawareness",
                },
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
            145: {
                "type": "chapter",
                "chapter_info": {
                    "name": "Appendix: Mindfulness in Brief",
                    "illumination_delimiter": "Sour",
                },
            },
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

    def convert_to_logical_page_number(self, page_number):
        if page_number == 0:
            return "Cover"
        # Deal with the first pages numbering that uses roman numeration
        if page_number >= 1 and page_number <= self.page_numbering_offset + 1:
            return roman.toRoman(page_number).lower()
        else:
            return page_number - self.page_numbering_offset

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

    def chapter_page_header(self, page_number):
        return (
            self._get_chapter_name(page_number)
            + r" \| "
            + str(self.convert_to_logical_page_number(page_number))
        )

    def book_title_page_header(self, page_number):
        return (
            str(self.convert_to_logical_page_number(page_number))
            + r" \| "
            + self.book_title
        )

    def get_page_header(self, page_number):

        if page_number < 0 or page_number > self.total_page_number:
            print("Page number is outside of book page numeration.")
            print("Exiting")
            sys.exit()

        # Pages explicitly flagged as headless, well, are headless:
        if self._page_is_headless(page_number):
            return ""

        # First headers of pages starting a new chapter have that new
        # chapter name as header
        if self._is_chapter_beginning_page(page_number):
            return self._get_chapter_name(page_number)

        ####### Concerning the Preamble (from page 0 to 20 included)
        # Before the body of the book, there is a (quite lengthy) preamble that
        # has quite specific header rules :
        if page_number < 10:
            # Default value for a preamble header is to be empty
            return ""
        if page_number >= 10 and page_number < 15:
            return roman.toRoman(page_number).lower()
        if page_number == 16:
            # The following hardcoded value for page 16 is because that page
            # doesn't follow the above logical rule. The following fix for page
            # 16 _is_ correct ! It is the pdf that is erroneous.
            return roman.toRoman(16).lower() + roman.toRoman(16).lower()
        if page_number == 17:
            return ""
        if page_number >= 18 and page_number < 20:
            return str(self.convert_to_logical_page_number(page_number))
        if page_number <= 19 and page_number <= 21:
            return ""

        ####### Concerning the body of the book.
        # Pages of the body of the book, have a headers that follow a simple
        # constructive rule with some exceptions...

        if (page_number % 2) == 0:
            # Odd pages have a header that is simply the book title followed
            # by their page number
            return self.book_title_page_header(page_number)
        if (page_number % 2) != 0:
            if page_number == 133:
                # Page 133 has a brain damaged header that doesn't
                # follow the even page header rule (although it is a near miss). The
                # only possible fix is to define an exception:
                return (
                    self.book_title
                    + self._get_chapter_name(133)
                    + " ||"
                    + str(self.convert_to_logical_page_number(133))
                    + str(self.convert_to_logical_page_number(133))
                )
            else:
                # Even pages have a different header pattern based on the current
                # chapter name
                return self.chapter_page_header(page_number)

        print("Header for page number ", page_number, " is not defined")
        print("Exiting")
        sys.exit()
