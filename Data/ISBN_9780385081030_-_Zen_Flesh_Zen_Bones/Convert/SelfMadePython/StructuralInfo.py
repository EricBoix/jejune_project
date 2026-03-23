from ConvertPdfToMarkdown import StructuralInfoBase


class StructuralInfo(StructuralInfoBase):
    # The structural information per se with extension specifics
    # - "type" can be "illustration" (with an optional "header" boolean flag)
    # - a "chapter_info" can have an optional "illumination_delimiter"

    def __init__(self):
        StructuralInfoBase.__init__(self)

        self.total_page_number = 209
        # FIXME: could the book_title be extracted automatically ?
        self.book_title = "ZEN FLESH, ZEN BONES"

        # Sub-chapters typically start with e.g. "85. Time to Die\n\n"
        self.superchapter_to_chapter_breaking_pattern = r"\d+\.[ ][A-Za-z| ]+"
        # The above pattern works and the chapter name that matches can be
        # safely extracted when this chapter appears at the head of a page.
        # But when the chapter happens in the middle of the page then they are
        # three \n in sequence to separate the chapters. A typical mid-page
        # chapter page is e.g.
        #                  "\n\n\n86. The Living Buddha and the Tubmaker\n\n"
        # The pattern thus becomes r"(\n\n\n)\d+\.[ ][A-Za-z| ]+"
        self.chapter_to_paragraph_breaking_pattern = r"\n\n  " + r"|" + r"\n\n"

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
