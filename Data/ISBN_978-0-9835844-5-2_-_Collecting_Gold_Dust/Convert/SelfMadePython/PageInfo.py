# The structural information constituted by the presence of chapters,
# illustrations, illumination, headers ... is quite often difficult
# to be automatically discovered. While waiting for better (and free)
# tools, the following was manually extracted and summarized in the
# following dictionary.

# Used for debug
total_page_number = 160

# The preamble section pages use roman numbering. This offsets the numbering
# of the body pages
page_numbering_offset = 16

# Concerning the format:
# - "type" is the {"chapter", "generic" "illustration"}
# - a "chapter" type must have a "chapter_info" dictionary

pages_info = {
    0: {
        # Artificial/fake chapter that is not explicitly defined in the
        # book. This is a technicality for the first pages not to be
        # devoid of belonging chapter:
        "type": "chapter",
        "chapter_info": {
            "name": "",
            "illumination_delimiter": None,
        },
        "drop_page": True,
    },
    1: {
        "type": "generic",
        # The content of the page is dropped (and won't be part of the
        # output)
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
        # The sting "\n    "
        "no_paragraphs": True,
    },
    6: {
        "type": "generic",
        "paragraph_fits_on_page": True,
    },
    7: {
        "type": "chapter",
        "chapter_info": {
            "name": "Acknowledgements",
            "illumination_delimiter": "MBhaddanta",
        },
        "paragraph_fits_on_page": True,
    },
    9: {
        "type": "chapter",
        "chapter_info": {
            "name": "Dear Reader",
            "illumination_delimiter": "Iobservation",
        },
    },
    10: {
        "type": "generic",
        # Notice that "practice." would be an erroneous delimiter:
        "first_paragraph_delimiter": "flagging practice.",
    },
    11: {
        "type": "generic",
        "first_paragraph_delimiter": "view.",
    },
    12: {
        "type": "generic",
        "first_paragraph_delimiter": "daily life.",
    },
    13: {
        "type": "generic",
        "first_paragraph_delimiter": "info@wisdomstreams.org.",
    },
    14: {
        "type": "generic",
        "first_paragraph_delimiter": "Tuck Loon.",
    },
    15: {
        "type": "chapter",
        "chapter_info": {
            "name": "On Language",
            "illumination_delimiter": "Wwords",
        },
    },
    16: {
        "type": "generic",
        "first_paragraph_delimiter": "wisdom.",
        # Required because next page is dropped
        "paragraph_fits_on_page": True,
    },
    17: {
        "type": "chapter",
        "chapter_info": {"name": "Contents", "illumination_delimiter": None},
        "paragraph_fits_on_page": True,
        "drop_page": True,
    },
    18: {
        "type": "generic",
        "paragraph_fits_on_page": True,
        "drop_page": True,
    },
    19: {
        "type": "generic",
        "paragraph_fits_on_page": True,
        "drop_page": True,
    },
    20: {
        "type": "illustration",  # Pure illustration (no text at all)
        "drop_page": True,
    },
    21: {
        "type": "chapter",
        "chapter_info": {
            "name": "A Note from the Teacher",
            "illumination_delimiter": "Ytime",
        },
    },
    22: {
        "type": "generic",
        "first_paragraph_delimiter": "wisdom.",
    },
    23: {
        "type": "generic",
        # Everything shorter would be wrong
        "first_paragraph_delimiter": "was that I was mindful.",
    },
    24: {
        "type": "illustration",  # illustration-with-extracted-text
        # Some illustration are decorated with text (or the other way round).
        # Yet this text is an extracted quote from the body of the chapter.
        # We can thus drop it without content loss.
        "drop_page": True,
    },
    25: {
        "type": "generic",
        "first_paragraph_delimiter": "discoveries.",
    },
    26: {
        "type": "generic",
        "first_paragraph_delimiter": "thing.",
    },
    27: {
        "type": "generic",
        "first_paragraph_delimiter": "do it.”",
    },
    28: {
        "type": "generic",
        "first_paragraph_delimiter": "center.",
    },
    29: {
        "type": "generic",
        "first_paragraph_delimiter": "depression.",
    },
    30: {
        "type": "illustration",  # illustration-with-extracted-text
        "drop_page": True,
    },
    31: {
        "type": "generic",
        "first_paragraph_delimiter": "resort.",
    },
    32: {
        "type": "generic",
        "first_paragraph_delimiter": "state.",
    },
    33: {
        "type": "generic",
        "first_paragraph_delimiter": "mind.",
    },
    34: {
        "type": "generic",
        "first_paragraph_delimiter": "emotions.",
    },
    35: {
        "type": "generic",
        "first_paragraph_delimiter": "disguise!",
        # We don't have to look for paragraph continuation on the next
        # page
        "paragraph_fits_on_page": True,
    },
    36: {
        "type": "illustration",  # illustration-with-extracted-text
        "drop_page": True,
    },
    37: {
        "type": "generic",
        "paragraph_fits_on_page": True,
    },
    # 38: well nothing to express
    39: {
        "type": "generic",
        "first_paragraph_delimiter": "time.",
        "paragraph_fits_on_page": True,
    },
    # 40: zilch
    41: {
        "type": "generic",
        "first_paragraph_delimiter": "himself.",
        "paragraph_fits_on_page": True,
    },
    42: {
        "type": "illustration",  # illustration-with-valid-text
        # This illustration has some additional textual content that is original
        # that is not part of the rest of the chapter text. We thus keep it.
    },
    43: {
        "type": "chapter",
        "chapter_info": {
            "name": "Mindfulness is a Lifestyle Change",
            "illumination_delimiter": "WTwo",
        },
    },
    44: {
        "type": "illustration",  # illustration-with-extracted-text
        "drop_page": True,
    },
    45: {
        "type": "generic",
        "first_paragraph_delimiter": "mind.",
        "paragraph_fits_on_page": True,
    },
    46: {
        "type": "generic",
        "paragraph_fits_on_page": True,
    },
    # 47: zilch
    48: {
        "type": "generic",
        "first_paragraph_delimiter": "business.",
        "paragraph_fits_on_page": True,
    },
    50: {
        "type": "illustration",  # illustration-with-extracted-text
        "drop_page": True,
    },
    51: {
        "type": "generic",
        "first_paragraph_delimiter": "suffering.",
        "paragraph_fits_on_page": True,
    },
    # 52: zilch
    53: {
        "type": "generic",
        "first_paragraph_delimiter": "day.",
        "paragraph_fits_on_page": True,
    },
    # 54: nada
    55: {
        "type": "generic",
        "first_paragraph_delimiter": "understanding.",
    },
    56: {
        "type": "illustration",  # illustration-with-extracted-text
        "drop_page": True,
    },
    57: {
        "type": "generic",
        "first_paragraph_delimiter": "habits.",
    },
    58: {
        "type": "generic",
        "first_paragraph_delimiter": "happen.",
    },
    59: {
        "type": "generic",
        "first_paragraph_delimiter": "effect.",
    },
    60: {
        "type": "generic",
        "first_paragraph_delimiter": "Understanding.",
        "paragraph_fits_on_page": True,
    },
    # 61: nichts
    62: {
        "type": "illustration",  # illustration-with-extracted-text
        "drop_page": True,
    },
    63: {
        "type": "generic",
        "first_paragraph_delimiter": "you.",
        "paragraph_fits_on_page": True,
    },
    64: {
        "type": "illustration",  # illustration-with-valid-text
    },
    65: {
        "type": "chapter",
        "chapter_info": {
            "name": "Take a Closer Look",
            "illumination_delimiter": "Man",
        },
    },
    66: {
        "type": "generic",
        "first_paragraph_delimiter": "vedanā.",
    },
    67: {
        "type": "generic",
        "first_paragraph_delimiter": "experience.",
        "paragraph_fits_on_page": True,
    },
    68: {
        "type": "illustration",  # illustration-with-extracted-text
        "drop_page": True,
    },
    # 69: this space intentionally left non void
    70: {
        "type": "generic",
        "first_paragraph_delimiter": "effects.",
        "paragraph_fits_on_page": True,
    },
    # 71: default is ok
    72: {
        "type": "generic",
        "first_paragraph_delimiter": "further.",
        "paragraph_fits_on_page": True,
    },
    73: {
        "type": "generic",
        "paragraph_fits_on_page": True,
    },
    74: {
        "type": "illustration",  # illustration-with-extracted-text
        "drop_page": True,
    },
    # 75: nothing
    76: {
        "type": "generic",
        "first_paragraph_delimiter": "happening.",
        "paragraph_fits_on_page": True,
    },
    77: {
        "type": "illustration",  # illustration-with-extracted-text
        "drop_page": True,
        # By default illustrations have no header, unless for some isolated
        # examples like the one on this page. Although the following flag is
        # correct, it is not useful for this entry since eventually the page
        # was dropped.
        "header": True,
    },
    78: {
        "type": "illustration",  # illustration-with-valid-text
    },
    79: {
        "type": "chapter",
        "chapter_info": {
            "name": "Reflect. Learn. Keep Going.",
            "illumination_delimiter": "Dnot",
        },
    },
    80: {
        "type": "generic",
        "first_paragraph_delimiter": "through.",
        "paragraph_fits_on_page": True,
    },
    # 81: nothing to say
    82: {
        "type": "illustration",  # illustration-with-extracted-text
        "drop_page": True,
    },
    83: {
        "type": "generic",
        "first_paragraph_delimiter": "process.",
    },
    84: {
        "type": "generic",
        "first_paragraph_delimiter": "uncomfortable.",
        "paragraph_fits_on_page": True,
    },
    # 85: nothing
    86: {
        "type": "generic",
        "first_paragraph_delimiter": "practice.",
    },
    87: {
        "type": "generic",
        "first_paragraph_delimiter": "or another.",
        "paragraph_fits_on_page": True,
    },
    88: {
        "type": "illustration",  # illustration-with-extracted-text
        "drop_page": True,
    },
    89: {
        "type": "generic",
        "paragraph_fits_on_page": True,
    },
    90: {
        "type": "illustration",  # illustration-with-valid-text
    },
    91: {
        "type": "chapter",
        "chapter_info": {
            "name": "Day-to-Day",
            "illumination_delimiter": "Wchange",
        },
    },
    92: {
        "type": "generic",
        "first_paragraph_delimiter": "term.",
        "paragraph_fits_on_page": True,
    },
    # 93: nothing to say
    94: {
        "type": "illustration",  # illustration-with-extracted-text
        "drop_page": True,
    },
    95: {
        "type": "generic",
        "first_paragraph_delimiter": "deepened.",
    },
    96: {
        "type": "generic",
        "first_paragraph_delimiter": "effect.",
        "paragraph_fits_on_page": True,
    },
    # 97: default
    98: {
        "type": "generic",
        "first_paragraph_delimiter": "people.",
        "paragraph_fits_on_page": True,
    },
    99: {
        "type": "generic",
        "paragraph_fits_on_page": True,
    },
    100: {
        "type": "illustration",  # illustration-with-extracted-text
        "drop_page": True,
    },
    # 101: dalmatians
    102: {
        "type": "generic",
        "first_paragraph_delimiter": "automatic.",
        "paragraph_fits_on_page": True,
    },
    # 103: default works
    104: {
        "type": "generic",
        "first_paragraph_delimiter": "time.",
    },
    105: {
        "type": "generic",
        "first_paragraph_delimiter": "well.",
    },
    106: {
        "type": "illustration",  # illustration-with-extracted-text
        "drop_page": True,
    },
    107: {
        "type": "generic",
        "first_paragraph_delimiter": ".",  # Notice the default case
    },
    108: {
        "type": "generic",
        "first_paragraph_delimiter": "steadier.",
    },
    109: {
        "type": "generic",
        "first_paragraph_delimiter": "silent?",
    },
    110: {
        "type": "generic",
        "first_paragraph_delimiter": "it.",
    },
    111: {
        "type": "generic",
        "first_paragraph_delimiter": "balanced.",
        "paragraph_fits_on_page": True,
    },
    112: {
        "type": "illustration",  # illustration-with-extracted-text
        "drop_page": True,
    },
    # 113: nothing
    114: {
        "type": "generic",
        "first_paragraph_delimiter": "understanding.",
        "paragraph_fits_on_page": True,
    },
    # 115: nothing
    116: {
        "type": "generic",
        "first_paragraph_delimiter": "violated.",
    },
    117: {
        "type": "generic",
        "first_paragraph_delimiter": "disappear.",
        "paragraph_fits_on_page": True,
    },
    118: {
        "type": "illustration",  # illustration-with-extracted-text
        "drop_page": True,
    },
    119: {
        "type": "generic",
        "paragraph_fits_on_page": True,
    },
    # 120: nothing
    121: {
        "type": "generic",
        "first_paragraph_delimiter": "people.",
    },
    122: {
        "type": "generic",
        "first_paragraph_delimiter": "deteriorate.",
    },
    123: {
        "type": "generic",
        "first_paragraph_delimiter": "way!",
        "paragraph_fits_on_page": True,
    },
    124: {
        "type": "illustration",
    },
    125: {
        "type": "chapter",
        "chapter_info": {
            "name": "A Lighter Approach",
            "illumination_delimiter": "Wawareness",
        },
        "paragraph_fits_on_page": True,
    },
    # 126: nothing
    127: {
        "type": "generic",
        "first_paragraph_delimiter": "life.",
    },
    128: {
        "type": "illustration",
    },
    129: {
        "type": "generic",
        "first_paragraph_delimiter": "habits.",
    },
    130: {
        "type": "generic",
        "first_paragraph_delimiter": "solutions.",
    },
    131: {
        "type": "generic",
        "first_paragraph_delimiter": "truth.",
    },
    132: {
        "type": "generic",
        "first_paragraph_delimiter": "lives.",
        "paragraph_fits_on_page": True,
    },
    133: {
        "type": "illustration",
        # By default illustrations have no header, unless ... they have
        "header": True,
    },
    134: {
        "type": "illustration",
    },
    135: {
        "type": "chapter",
        "chapter_info": {
            "name": "Continuing the Work",
            "illumination_delimiter": "A remember",
        },
    },
    136: {
        "type": "generic",
        "first_paragraph_delimiter": "moment.",
        "paragraph_fits_on_page": True,
    },
    137: {
        "type": "generic",
        "first_paragraph_delimiter": "Thought.",
        "paragraph_fits_on_page": True,
    },
    138: {
        "type": "illustration",
    },
    # 139
    140: {
        "type": "generic",
        "first_paragraph_delimiter": "perspective.",
    },
    141: {
        "type": "generic",
        "first_paragraph_delimiter": ".",  # End of first sentence
    },
    142: {
        "type": "generic",
        "first_paragraph_delimiter": "useful.",
    },
    143: {
        "type": "generic",
        "first_paragraph_delimiter": "operate.",
        "paragraph_fits_on_page": True,
    },
    144: {
        "type": "illustration",
    },
    145: {
        "type": "chapter",
        "chapter_info": {
            "name": "Appendix: Mindfulness in Brief",
            "illumination_delimiter": "Sour",
        },
    },
    146: {
        "type": "generic",
        "first_paragraph_delimiter": "the mind.",
    },
    147: {
        "type": "generic",
        "first_paragraph_delimiter": "mind.",
        "paragraph_fits_on_page": True,
    },
    148: {
        "type": "generic",
        "paragraph_fits_on_page": True,
    },
    149: {
        "type": "generic",
        "paragraph_fits_on_page": True,
    },
    150: {
        "type": "illustration",
    },
    # 151
    152: {
        "type": "generic",
        "first_paragraph_delimiter": ".",
        "paragraph_fits_on_page": True,
    },
    153: {
        "type": "generic",
        "paragraph_fits_on_page": True,
    },
    154: {
        "type": "generic",
        "paragraph_fits_on_page": True,
    },
    # 155
    156: {
        "type": "illustration",
    },
    157: {
        "type": "generic",
        "first_paragraph_delimiter": "learn.",
        "paragraph_fits_on_page": True,
    },
    158: {
        "type": "chapter",
        "chapter_info": {"name": "Dedication", "illumination_delimiter": None},
        "paragraph_fits_on_page": True,
    },
    159: {
        # This is the back cover of the book
        "type": "illustration",
    },
}
