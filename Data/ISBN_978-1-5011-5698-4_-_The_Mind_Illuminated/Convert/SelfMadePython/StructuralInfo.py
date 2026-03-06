import re

from ConvertPdfToMarkdown import StructuralInfoBase


class StructuralInfo(StructuralInfoBase):
    """
    Nothing specific to this structural information that only uses the standard
    notions of StructuralInfoBase.
    """

    def __init__(self):
        StructuralInfoBase.__init__(self)
        self.total_page_number = 578
        # The original pdf document has a title that is depicted (as opposed to
        # written in text) in the cover illustration and thus cannot be
        # automatically extracted.
        self.book_title = "The MIND ILLUMINATED: A Complete Meditation Guide Integrating Buddhist Wisdom and Brain Science for Greater Mindfulness"
        self.chapter_to_paragraph_breaking_pattern = "\n   "
        self.pages_info = {
            0: {
                # The cover page being pure illustration (no text), its
                # (absence of) content is dropped.
                "drop_page": True,
            },
            1: {"drop_page": True},
            2: {"drop_page": True},
            3: {"drop_page": True},
            4: {"drop_page": True},
            5: {"drop_page": True},  # Skip the "Contents" chapter/pages
            6: {"drop_page": True},
            7: {"drop_page": True},
            8: {"drop_page": True},  # Skip the "List of Figures" chapter/pages
            9: {"drop_page": True},
            # 10: "chapter_info": { "name": "Foreword" }
            15: {"type": "generic", "paragraph_fits_on_page": True},
            26: {"type": "generic", "paragraph_fits_on_page": True},
            28: {"type": "generic", "paragraph_fits_on_page": True},
            43: {"type": "generic", "paragraph_fits_on_page": True},
            44: {"type": "generic", "paragraph_fits_on_page": True},
            45: {"type": "generic", "paragraph_fits_on_page": True},
            49: {"type": "generic", "paragraph_fits_on_page": True},
            53: {"type": "generic", "paragraph_fits_on_page": True},
            72: {"type": "generic", "paragraph_fits_on_page": True},
            73: {"type": "generic", "paragraph_fits_on_page": True},
            76: {"type": "generic", "paragraph_fits_on_page": True},
            77: {"type": "generic", "paragraph_fits_on_page": True},
            78: {"type": "generic", "paragraph_fits_on_page": True},
            86: {"type": "generic", "paragraph_fits_on_page": True},
            108: {"type": "generic", "paragraph_fits_on_page": True},
            # All the following chapter definitions are required because
            # otherwise one gets an error message of the form :
            #    unable to find the last paragraph of page number  126
            #    in chapter SECOND INTERLUDE
            127: {
                "type": "chapter",
                "chapter_info": {"name": "STAGE THREE"},
            },
            130: {"type": "generic", "paragraph_fits_on_page": True},
            138: {"type": "generic", "paragraph_fits_on_page": True},
            143: {"type": "generic", "paragraph_fits_on_page": True},
            147: {"type": "generic", "paragraph_fits_on_page": True},
            159: {"type": "generic", "paragraph_fits_on_page": True},
            162: {
                "type": "chapter",
                "chapter_info": {"name": "STAGE FOUR"},
            },
            166: {"type": "generic", "paragraph_fits_on_page": True},
            168: {"type": "generic", "paragraph_fits_on_page": True},
            174: {"type": "generic", "paragraph_fits_on_page": True},
            176: {"type": "generic", "paragraph_fits_on_page": True},
            179: {"type": "generic", "paragraph_fits_on_page": True},
            184: {"type": "generic", "paragraph_fits_on_page": True},
            186: {"type": "generic", "paragraph_fits_on_page": True},
            203: {"type": "generic", "paragraph_fits_on_page": True},
            209: {"type": "generic", "paragraph_fits_on_page": True},
            211: {"type": "generic", "paragraph_fits_on_page": True},
            213: {"type": "generic", "paragraph_fits_on_page": True},
            228: {"type": "generic", "paragraph_fits_on_page": True},
            239: {"type": "generic", "paragraph_fits_on_page": True},
            262: {"type": "generic", "paragraph_fits_on_page": True},
            294: {"type": "generic", "paragraph_fits_on_page": True},
            307: {"type": "generic", "paragraph_fits_on_page": True},
            347: {"type": "generic", "paragraph_fits_on_page": True},
            351: {"type": "generic", "paragraph_fits_on_page": True},
            364: {"type": "generic", "paragraph_fits_on_page": True},
            380: {"type": "generic", "paragraph_fits_on_page": True},
            391: {
                "type": "chapter",
                "chapter_info": {"name": "STAGE NINE"},
            },
            406: {"type": "generic", "paragraph_fits_on_page": True},
            434: {"type": "generic", "paragraph_fits_on_page": True},
            440: {"type": "generic", "paragraph_fits_on_page": True},
            452: {"type": "generic", "paragraph_fits_on_page": True},
            473: {"type": "generic", "paragraph_fits_on_page": True},
            475: {"type": "generic", "paragraph_fits_on_page": True},
            478: {"drop_page": True},
            479: {
                "type": "chapter",
                "chapter_info": {"name": "Glossary"},
            },
            482: {"type": "generic", "paragraph_fits_on_page": True},
            484: {"type": "generic", "paragraph_fits_on_page": True},
            486: {"type": "generic", "paragraph_fits_on_page": True},
            488: {"type": "generic", "paragraph_fits_on_page": True},
            490: {"type": "generic", "paragraph_fits_on_page": True},
            # Starting from 519 we are in the Index. We should be dropping the
            # following content instead of continuing its treatment
            549: {"type": "generic", "paragraph_fits_on_page": True},
            571: {"type": "generic", "paragraph_fits_on_page": True},
        }

    def convert_to_logical_page_number(self, page_number):
        if page_number == 0:
            return "Cover"
        return page_number
