import re
from typing import Optional
from ConvertPdfToMarkdown import (
    ChapterSplitter,
    NameLessSinglePatternSplitter,
    StructuralInfoBase,
    SinglePatternSplitter,
    WarnAndExit,
)
from Sanitizer import Sanitizer


class StructuralInfo(StructuralInfoBase):
    """
    Nothing specific to this structural information that only uses the standard
    notions of StructuralInfoBase.
    """

    class chapter_splitter(ChapterSplitter):
        """Chapter splitter for The Mind Illuminated.

        Detects chapter boundaries based on:
        1. Static declarations in pages_info (type == "chapter")
        2. Multiple newlines followed by text
        """

        def __init__(self, structural_info):
            structural_info = structural_info
            chapter_name_separator_regex = r"((?:\n){3,}(\w| ))"
            chapter_name_separator_first_occurrence = 100
            ChapterSplitter.__init__(
                self,
                structural_info,
                chapter_name_separator_regex,
                chapter_name_separator_regex,  # Extractor = Separator
                chapter_name_separator_first_occurrence,
            )

    class superchapter_to_chapter_splitter(SinglePatternSplitter):
        def __init__(self):
            # Sub-chapters are typically of the form e.g.
            #     \nMEDITATION: THE SCIENCE AND ART OF LIVING\n
            #     \nPUTTING THIS PRACTICE INTO CONTEXT\n
            # We thus need to define three parts for the pattern
            # 1. the ante chapter breaking lines
            ante_pattern = r"\n"
            # 2. the name of the chapter per se. Note that the minimum number
            # for matching has to be
            # - at least 2 in order not to match the first (capital letter of
            #   a sentence) e.g. "Stand by me."
            # - at least three not to match e.g. "A cat was run over." where the
            #   the initial capital and its following whitespace would match.
            # For the upper limit to, well a full line should suffice.
            name_pattern = r"[A-Z|:| ]{3,100}"
            # 3. the trailing return
            post_pattern = r"\n"
            breaking_pattern = ante_pattern + name_pattern + post_pattern
            SinglePatternSplitter.__init__(self, breaking_pattern, name_pattern)

    class chapter_to_paragraph_splitter(NameLessSinglePatternSplitter):
        def __init__(self):
            breaking_pattern = "\n   "
            NameLessSinglePatternSplitter.__init__(self, breaking_pattern)

    @property
    def total_page_number(self) -> int:
        return 578

    def __init__(self):
        StructuralInfoBase.__init__(self)
        self._sanitizer = Sanitizer()
        # The original pdf document has a title that is depicted (as opposed to
        # written in text) in the cover illustration and thus cannot be
        # automatically extracted.
        self.book_title = "The MIND ILLUMINATED: A Complete Meditation Guide Integrating Buddhist Wisdom and Brain Science for Greater Mindfulness"

        self._pages_info = {
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
            130: {"type": "generic", "paragraph_fits_on_page": True},
            138: {"type": "generic", "paragraph_fits_on_page": True},
            143: {"type": "generic", "paragraph_fits_on_page": True},
            147: {"type": "generic", "paragraph_fits_on_page": True},
            159: {"type": "generic", "paragraph_fits_on_page": True},
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
            406: {"type": "generic", "paragraph_fits_on_page": True},
            434: {"type": "generic", "paragraph_fits_on_page": True},
            440: {"type": "generic", "paragraph_fits_on_page": True},
            452: {"type": "generic", "paragraph_fits_on_page": True},
            473: {"type": "generic", "paragraph_fits_on_page": True},
            475: {"type": "generic", "paragraph_fits_on_page": True},
            478: {"drop_page": True},
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

    @property
    def pages_info(self) -> dict:
        return self._pages_info

    def convert_to_logical_page_number(self, page_number):
        if page_number == 0:
            return "Cover"
        return str(page_number)

    def sanitize_page_text(self, extracted_page):
        self._sanitizer.sanitize_page_text(extracted_page)
