# Inferring pattern rules to recognize a chapter, sub-chapter, figures

The multiple successive occurrence of the "\n" character (newline) indicates the remains of some lost pdf structure like chapters, sub-chapters, figures. In order to retrieve
The exploration is done with some editor (e.g. vim) where one discovers that
chapter names appear after a sequence of at least three \n characters i.e.
newline. Here are some vim search patterns that proved useful when searching
for chapter name occurrences:

- /\\n\\n\\n\(\\n\)*[a-zA-Z]    : at least three \n followed by any                                   alphabetical character
- /\\n\\n\(\\n\)*[ ]            : at least two \n followed by a whitespace
- /\\n\\n\\n\\n\(\\n\)*Figure   : at least four \n followed by the "Figure"                                  string

## Chapters

Exactly three \n followed by an alphabetical character denote a possible chapter name

- "Foreword\n\n\nSO\t HOW\t does"
- "Introduction\n\n\nMY\tPURPOSE\tin"

Yet they are some occurrences with more than three '\n' like

- "Glossary\n\n\n\n\n\nAccess\t concentration"
- "Notes\n\n\n\n\nINTRODUCTION"
- "Index\n\n\n\n\n\nA\tnote\tabout"

And also the sequence of '\n' can be of variable length. Besides it is not always followed by an alphabetical character but sometimes with a whitespace. Here are some examples

- "STAGE\tONE\nEstablishing\ta\tPractice\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n    The\tgoal"
- "STAGE\tTWO\nInterrupted\tAttention\tand\tOvercoming\tMind-\nWandering\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n    The"
- "STAGE\tSEVEN\nExclusive\tAttention\tand\tUnifying\tthe\tMind\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n    The\tgoal"
- "STAGE\tTEN\nTranquility\tand\tEquanimity\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n    The\tgoal\tof\tStage"
- "Final\tThoughts\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n    The\tgoal\tbeyond\tStage"

## Figures

Note: vi search pattern '\\n\\n\\\n\\n\\n\\n\\n\\n\\n\\n\\n\\n\\n\\n\\n\\n\\n\\n\\n\\n\\n\\n\\n\\n\\n\\n\\n\\n\\n\\n\\n\\nFigure'

Examples:

When the 'Figure' string appears at the top a page, the preceding '\n' are omitted e.g.

- "Figure\t1.\tProg"
- "Figure 57. Thr"

Just as for chapters, there can be a variable number of '\n' occurring before 'Figure' e.g.

- "ime.\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nFigure\t3.\tG"
- "ity.\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nFigure 55. Prior"
- "ack.\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nFigure\t20."
- "way.\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nFigure 28."
  