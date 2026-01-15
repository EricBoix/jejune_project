# The structural information constituted by the presence of chapters,
# illustrations, illumination, headers ... is quite often difficult
# to be automatically discovered. While waiting for better (and free)
# tools, the following was manually extracted and summarized in the
# following dictionary.

# Used for debug
total_page_number = 578

# Concerning the format:
# - the integer index is the page_number as used by pdf's
#   PdfReader.get_page(page_number) method which is a vector index and as such
#   starts at 0 (the notation .pages[page_number] being preferred)
# - "type" is the {"chapter", "generic" "illustration"}
# - a "chapter" type must have a "chapter_info" dictionary

pages_info = {
    0: {
        "type": "illustration",  # The cover page is pure illustration
        # The content of the page is dropped (and won't be part of the
        # output)
        "drop_page": True,
    },
    1: {
        "type": "generic",
        "drop_page": True,
    },
    2: {
        "type": "illustration",  # Pure illustration
        "drop_page": True,
    },
    3: {
        "type": "generic",
        "paragraph_fits_on_page": True,
    },
    4: {
        "type": "generic",
        "drop_page": True,
    },
    5: {
        "type": "generic",
        "paragraph_fits_on_page": True,
    },
    6: {
        "type": "generic",
        "paragraph_fits_on_page": True,
    },
    7: {
        "type": "generic",
        "paragraph_fits_on_page": True,
    },
    8: {
        "type": "chapter",
        "chapter_info": {
            "name": "List of Figures",
        },
        "paragraph_fits_on_page": True,
    },
    9: {
        "type": "generic",
        "paragraph_fits_on_page": True,
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
        "chapter_info": {
            "name": "FIRST INTERLUDE",
        },
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
        "chapter_info": {
            "name": "STAGE ONE",
        },
    },
    94: {
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
    151: {
        "type": "chapter",
        "chapter_info": {
            "name": "THIRD INTERLUDE",
        },
    },
    162: {
        "type": "chapter",
        "chapter_info": {
            "name": "STAGE FOUR",
        },
    },
    196: {
        "type": "chapter",
        "chapter_info": {
            "name": "FOURTH INTERLUDE",
        },
    },
    218: {
        "type": "chapter",
        "chapter_info": {
            "name": "STAGE FIVE",
        },
    },
    232: {
        "type": "chapter",
        "chapter_info": {
            "name": "FIFTH INTERLUDE",
        },
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
    318: {
        "type": "chapter",
        "chapter_info": {
            "name": "STAGE SEVEN",
        },
    },
}
