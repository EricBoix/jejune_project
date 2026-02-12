class StructuralInfo:
    """
    The structural information constituted by the presence of chapters,
    illustrations, illumination, headers ... is quite often difficult
    to be automatically discovered. While waiting for better (and free)
    tools, the following was manually extracted and summarized in the
    following dictionary.

    Concerning the format:
    - the integer index is the page_number as used by pdf's
      PdfReader.get_page(page_number) method which is a vector index and as such
      starts at 0 (the notation .pages[page_number] being preferred)
    - "type" is among {"chapter", "generic" "illustration"}
    - a "chapter" type must have a "chapter_info" dictionary
    """

    def __init__(self):
        self.total_page_number = 578
        self.chapter_to_paragraph_breaking_pattern = "\n   "
        self.pages_info = {
            0: {
                "type": "illustration",  # The cover page is pure illustration
                # The content of the page is dropped (and won't be part of the
                # output)
                "drop_page": True,
            },
            1: {
                "drop_page": True,
            },
            2: {
                "drop_page": True,
            },
            3: {
                "drop_page": True,
            },
            4: {
                "drop_page": True,
            },
            # Skip the "Contents" chapter/pages
            5: {
                "drop_page": True,
            },
            6: {
                "drop_page": True,
            },
            7: {
                "drop_page": True,
            },
            # Skip the "List of Figures" chapter/pages
            8: {
                "drop_page": True,
            },
            9: {
                "drop_page": True,
            },
            10: {
                "type": "chapter",
                "chapter_info": {
                    "name": "Foreword",
                },
            },
            11: {
                "type": "generic",
            },
            12: {
                "type": "generic",
            },
            13: {
                "type": "generic",
            },
            14: {
                "type": "generic",
            },
            15: {
                "type": "generic",
                "paragraph_fits_on_page": True,
            },
            16: {
                "type": "chapter",
                "chapter_info": {"name": "Introduction"},
            },
            26: {
                "type": "generic",
                "paragraph_fits_on_page": True,
            },
            27: {
                "type": "chapter",
                "chapter_info": {"name": "An Overview of the Ten Stages"},
            },
            28: {
                "type": "generic",
                "paragraph_fits_on_page": True,
            },
            43: {
                "type": "generic",
                "paragraph_fits_on_page": True,
            },
            44: {
                "type": "generic",
                "paragraph_fits_on_page": True,
            },
            45: {
                "type": "generic",
                "paragraph_fits_on_page": True,
            },
            46: {
                "type": "chapter",
                "chapter_info": {"name": "FIRST INTERLUDE"},
            },
            49: {
                "type": "generic",
                "paragraph_fits_on_page": True,
            },
            53: {
                "type": "generic",
                "paragraph_fits_on_page": True,
            },
            69: {
                "type": "chapter",
                "chapter_info": {"name": "STAGE ONE"},
            },
            72: {
                "type": "generic",
                "paragraph_fits_on_page": True,
            },
            73: {
                "type": "generic",
                "paragraph_fits_on_page": True,
            },
            76: {
                "type": "generic",
                "paragraph_fits_on_page": True,
            },
            77: {
                "type": "generic",
                "paragraph_fits_on_page": True,
            },
            78: {
                "type": "generic",
                "paragraph_fits_on_page": True,
            },
            86: {
                "type": "generic",
                "paragraph_fits_on_page": True,
            },
            95: {
                "type": "chapter",
                "chapter_info": {
                    "name": "SECOND INTERLUDE",
                },
            },
            108: {
                "type": "generic",
                "paragraph_fits_on_page": True,
            },
            109: {
                "type": "chapter",
                "chapter_info": {
                    "name": "STAGE TWO",
                },
            },
            127: {
                "type": "chapter",
                "chapter_info": {
                    "name": "STAGE THREE",
                },
            },
            130: {
                "type": "generic",
                "paragraph_fits_on_page": True,
            },
            138: {
                "type": "generic",
                "paragraph_fits_on_page": True,
            },
            143: {
                "type": "generic",
                "paragraph_fits_on_page": True,
            },
            147: {
                "type": "generic",
                "paragraph_fits_on_page": True,
            },
            151: {
                "type": "chapter",
                "chapter_info": {
                    "name": "THIRD INTERLUDE",
                },
            },
            159: {
                "type": "generic",
                "paragraph_fits_on_page": True,
            },
            162: {
                "type": "chapter",
                "chapter_info": {
                    "name": "STAGE FOUR",
                },
            },
            166: {
                "type": "generic",
                "paragraph_fits_on_page": True,
            },
            168: {
                "type": "generic",
                "paragraph_fits_on_page": True,
            },
            174: {
                "type": "generic",
                "paragraph_fits_on_page": True,
            },
            176: {
                "type": "generic",
                "paragraph_fits_on_page": True,
            },
            179: {
                "type": "generic",
                "paragraph_fits_on_page": True,
            },
            184: {
                "type": "generic",
                "paragraph_fits_on_page": True,
            },
            186: {
                "type": "generic",
                "paragraph_fits_on_page": True,
            },
            196: {
                "type": "chapter",
                "chapter_info": {
                    "name": "FOURTH INTERLUDE",
                },
            },
            203: {
                "type": "generic",
                "paragraph_fits_on_page": True,
            },
            209: {
                "type": "generic",
                "paragraph_fits_on_page": True,
            },
            211: {
                "type": "generic",
                "paragraph_fits_on_page": True,
            },
            213: {
                "type": "generic",
                "paragraph_fits_on_page": True,
            },
            218: {
                "type": "chapter",
                "chapter_info": {
                    "name": "STAGE FIVE",
                },
            },
            228: {
                "type": "generic",
                "paragraph_fits_on_page": True,
            },
            232: {
                "type": "chapter",
                "chapter_info": {
                    "name": "FIFTH INTERLUDE",
                },
            },
            239: {
                "type": "generic",
                "paragraph_fits_on_page": True,
            },
            262: {
                "type": "generic",
                "paragraph_fits_on_page": True,
            },
            270: {
                "type": "chapter",
                "chapter_info": {
                    "name": "STAGE SIX",
                },
            },
            291: {
                "type": "chapter",
                "chapter_info": {
                    "name": "SIXTH INTERLUDE",
                },
            },
            294: {
                "type": "generic",
                "paragraph_fits_on_page": True,
            },
            307: {
                "type": "generic",
                "paragraph_fits_on_page": True,
            },
            318: {
                "type": "chapter",
                "chapter_info": {
                    "name": "STAGE SEVEN",
                },
            },
            347: {
                "type": "generic",
                "paragraph_fits_on_page": True,
            },
            351: {
                "type": "generic",
                "paragraph_fits_on_page": True,
            },
            360: {
                "type": "chapter",
                "chapter_info": {
                    "name": "STAGE EIGHT",
                },
            },
            364: {
                "type": "generic",
                "paragraph_fits_on_page": True,
            },
            380: {
                "type": "generic",
                "paragraph_fits_on_page": True,
            },
            391: {
                "type": "chapter",
                "chapter_info": {
                    "name": "STAGE NINE",
                },
            },
            402: {
                "type": "chapter",
                "chapter_info": {
                    "name": "STAGE TEN",
                },
            },
            406: {
                "type": "generic",
                "paragraph_fits_on_page": True,
            },
            407: {
                "type": "chapter",
                "chapter_info": {
                    "name": "Final Thoughts",
                },
            },
            412: {
                "type": "chapter",
                "chapter_info": {
                    "name": "Acknowledgments",
                },
            },
            414: {
                "type": "chapter",
                "chapter_info": {
                    "name": "APPENDIX A\nWalking Meditation",
                },
            },
            427: {
                "type": "chapter",
                "chapter_info": {
                    "name": "APPENDIX B\nAnalytical Meditation",
                },
            },
            434: {
                "type": "generic",
                "paragraph_fits_on_page": True,
            },
            435: {
                "type": "chapter",
                "chapter_info": {
                    "name": "APPENDIX C\nLoving-Kindness Meditation",
                },
            },
            440: {
                "type": "generic",
                "paragraph_fits_on_page": True,
            },
            441: {
                "type": "chapter",
                "chapter_info": {
                    "name": "APPENDIX D\nThe Jhānas",
                },
            },
            452: {
                "type": "generic",
                "paragraph_fits_on_page": True,
            },
            461: {
                "type": "chapter",
                "chapter_info": {
                    "name": "APPENDIX E\nMindful Review",
                },
            },
            473: {
                "type": "generic",
                "paragraph_fits_on_page": True,
            },
            475: {
                "type": "generic",
                "paragraph_fits_on_page": True,
            },
            476: {
                "type": "chapter",
                "chapter_info": {
                    "name": "About the Authors",
                },
            },
            478: {
                "type": "generic",
                # The content of the page is dropped (and won't be part of the
                # output)
                "drop_page": True,
            },
            479: {
                "type": "chapter",
                "chapter_info": {
                    "name": "Glossary",
                },
            },
            482: {
                "type": "generic",
                "paragraph_fits_on_page": True,
            },
            484: {
                "type": "generic",
                "paragraph_fits_on_page": True,
            },
            486: {
                "type": "generic",
                "paragraph_fits_on_page": True,
            },
            488: {
                "type": "generic",
                "paragraph_fits_on_page": True,
            },
            490: {
                "type": "generic",
                "paragraph_fits_on_page": True,
            },
            492: {
                "type": "chapter",
                "chapter_info": {
                    "name": "Notes",
                },
            },
            # Starting from 519 we are in the Index. We should be dropping the
            # following content instead of continuing its treatment
            549: {
                "type": "generic",
                "paragraph_fits_on_page": True,
            },
            571: {
                "type": "generic",
                "paragraph_fits_on_page": True,
            },
        }
