# Extracting the book semantic structure out of Collecting Gold Dust book<!-- omit from toc -->

## Table of contents<!-- omit from toc -->

- [Introduction](#introduction)
- [Running things](#running-things)
- [Testing](#testing)
- [Peculiarities and things to fix](#peculiarities-and-things-to-fix)

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
Notice that both sentence comme from a quote that in the PDF are highlighted with an italic mode that is lost by the pdf to text converter.
