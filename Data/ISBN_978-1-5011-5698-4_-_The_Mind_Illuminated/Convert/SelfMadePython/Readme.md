# Extracting the book semantic structure out of Collecting Gold Dust book<!-- omit from toc -->

## Table of contents<!-- omit from toc -->

- [Introduction](#introduction)
- [Running things](#running-things)
- [Testing](#testing)
- [Peculiarities and things to fix](#peculiarities-and-things-to-fix)
- [Helpers to infer pattern rules to recognize/extract a chapter, sub-chapter, figures](#helpers-to-infer-pattern-rules-to-recognizeextract-a-chapter-sub-chapter-figures)

## Introduction

This directory holds a a modified copy of the Python code used to convert Collecting Gold Dust.
Refer to the [original directory for design notes](../../../ISBN_978-0-9835844-5-2_-_Collecting_Gold_Dust/Readme.md#extracting-the-book-semantic-structure-out-of-collecting-gold-dust-book)...

## Running things

```bash
cd `git rev-parse --show-toplevel`/Data/ISBN_978-1-5011-5698-4_-_The_Mind_Illuminated/Convert/SelfMadePython
python3.10 -m venv venv
source ./venv/bin/activate
pip install -r ../../../requirements.txt
pip install ../../../ConvertPdfToMarkdown
python main.py
```

## Testing

Within the above running context (directory and installed virtual environment)

```bash
pytest test_main.py
```

## Peculiarities and things to fix

- The original text (as gotten in `ExtractedPage::__init__` within the `original_page_text` temporary variable ) goes `Final\tThoughts\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n    The\tgoal\tbeyond\tStage`. This 21 long repetition of `\n` is a singular occurrence (either from the pdf document or the pdf reader) that messes things down the road: in particular, a nasty side effect is that it ends up creating empty paragraphs...
- On page 86, the sentence `You’ll have to overcome four major obstacles: not enough time, \nprocrastination, reluctance and resistance to practicing, and doubt.` ends up split in two. Indeed there is a `\n` in the original text. Yet couldn't we improve on things by detecting that the first part of the sentence is not finished (not trailing punctuation) whereas the second part is not properly started (missing upper case) ?  
This is the same for the sentence `The practical steps: choose a suitable time and place, find the posture \nthat’s best for you, cultivate the right attitude, and generate strong\nmotivation.` that gets split in three (on page 90).  
Notice that both sentences comme from a quote that in the PDF are highlighted with an italic mode that is lost by the pdf to text converter.
- On page 34 a sub-paragraph is name `\nSTAGE TWO: INTERRUPTED ATTENTION AND OVERCOMING MIND-\nWANDERING\n` that includes a `\n`. This confuses the splitter that ends up considering that the sub-chapter title is simply `WANDERING`. Other examples:
- `\nSTAGE FOUR:\tCONTINUOUS ATTENTION\tAND\tOVERCOMING GROSS\nDISTRACTION AND STRONG DULLNESS\n` on page 36,
- `\nSTAGE FIVE: OVERCOMING SUBTLE DULLNESS AND INCREASING\nMINDFULNESS\n` on page 36,
- `\nSTAGE NINE: MENTAL AND PHYSICAL PLIANCY AND CALMING THE INTENSITY\nOF MEDITATIVE JOY\n` on page 40...

## Helpers to infer pattern rules to recognize/extract a chapter, sub-chapter, figures

The multiple successive occurrence of the `\n` character (newline) indicates the remains of some lost pdf structure like chapters, sub-chapters, figures. In order to retrieve those patterns some manual exploration is done with some editor (e.g. vim) where one discovers that chapter names appear after a sequence of at least three `\n` characters i.e. newline. Here are some vim search patterns that proved useful when searching for chapter name occurrences:

- `/\\n\\n\\n\(\\n\)*[a-zA-Z]`    : at least three `\n` followed by any alphabetical character
- `/\\n\\n\(\\n\)*[ ]`            : at least two `\n` followed by a whitespace
- `/\\n\\n\\n\\n\(\\n\)*Figure`   : at least four `\n` followed by the "Figure" string

### Concerning Chapters

Exactly three \n followed by an alphabetical character denote a possible chapter name

- `Foreword\n\n\nSO\t HOW\t does`
- `Introduction\n\n\nMY\tPURPOSE\tin`

Yet they are some occurrences with more than three '\n' like

- `Glossary\n\n\n\n\n\nAccess\t concentration`
- `Notes\n\n\n\n\nINTRODUCTION`
- `Index\n\n\n\n\n\nA\tnote\tabout`

And also the sequence of '\n' can be of variable length. Besides it is not always followed by an alphabetical character but sometimes with a whitespace. Here are some examples

- `STAGE\tONE\nEstablishing\ta\tPractice\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n    The\tgoal`
- `STAGE\tTWO\nInterrupted\tAttention\tand\tOvercoming\tMind-\nWandering\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n    The`
- `STAGE\tSEVEN\nExclusive\tAttention\tand\tUnifying\tthe\tMind\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n    The\tgoal`
- `STAGE\tTEN\nTranquility\tand\tEquanimity\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n    The\tgoal\tof\tStage`
- `Final\tThoughts\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n    The\tgoal\tbeyond\tStage`

### Concerning Figures

Note: vi search pattern `\\n\\n\\\n\\n\\n\\n\\n\\n\\n\\n\\n\\n\\n\\n\\n\\n\\n\\n\\n\\n\\n\\n\\n\\n\\n\\n\\n\\n\\n\\n\\n\\nFigure`

When the 'Figure' string appears at the top a page, the preceding `\n` are omitted e.g.

- `Figure\t1.\tProg`
- `Figure 57. Thr`

Just as for chapters, there can be a variable number of `\n` occurring before 'Figure' e.g.

- `ime.\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nFigure\t3.\tG`
- `ity.\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nFigure 55. Prior`
- `ack.\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nFigure\t20.`
- `way.\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nFigure 28.`