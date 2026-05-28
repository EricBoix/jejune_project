# Extracting the book semantic structure out of Collecting Gold Dust book<!-- omit from toc -->

## Table of contents<!-- omit from toc -->

- [Introduction](#introduction)
- [Running things](#running-things)
- [Testing](#testing)
- [To be fixed](#to-be-fixed)

## Introduction

This directory holds a [copy of the pdf version of Sayadaw U Tejaniya's book
COLLECTING GOLD DUST Nurturing the Dhamma in Daily Living](./original_data/2019_-_Sayadaw-U-Tejaniya-Collecting-Gold-Dust-Web-Book-1.pdf) as offered e.g. by [this Scribd link](https://www.scribd.com/document/716383730/Collecting-Gold-Dust-Web-Book-1)

## Running things

```bash
cd `git rev-parse --show-toplevel`/Data/ISBN_978-0-9835844-5-2_-_Collecting_Gold_Dust/Convert/SelfMadePython
python3.10 -m venv venv
source ./venv/bin/activate
pip install -r ../../../requirements.txt
pip install git+https://github.com/EricBoix/pdf-to-markdown.git
python main.py
```

Also refer to [`data_production.py`](../../data_production.py) script for usage examples.

## Testing

Within the above running context (directory and installed virtual environment)

```bash
pytest test_main.py
```

## To be fixed

- Some word get modified during extraction: within `output.md` look for
  - the word `eperience` that was initially properly spelled in the sentence `discussing their experiences and discoveries`.
  - the word `ecitement` that was initially properly spelled in the sentence `excitement calming down`
- Some subchapters (quite a few actually) are erroneous. For example the original text doesn't have chapter named `A CAUSE AND EFFECT CHAIN` or `| |`...
