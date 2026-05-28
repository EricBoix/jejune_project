# Extracting the book semantic structure out of Collecting Gold Dust book<!-- omit from toc -->

## Table of contents<!-- omit from toc -->

- [Introduction](#introduction)
- [Running things](#running-things)
- [Testing](#testing)
- [Peculiarities and things to fix](#peculiarities-and-things-to-fix)

## Introduction

This [pdf book version](../../Readme.md) particularities

- page numbering (at all)

## Running things

```bash
cd `git rev-parse --show-toplevel`/Data/ISBN_9780385081030_-_Zen_Flesh_Zen_Bones/Convert/SelfMadePython
python3.10 -m venv venv
source ./venv/bin/activate
pip install -r ../../../requirements.txt
pip install git+https://github.com/EricBoix/pdf-to-markdown.git
python main.py
```

## Testing

Within the above running context (directory and installed virtual environment)

```bash
pytest test_main.py
```

## Peculiarities and things to fix

- Page 15 finishes with the following sentence:
  
  ```text
  ‘I am Gudo of Kyoto and I am going on to Edo,’ replied the Zen master.
  ```

  gets rejected by `Sentence::is_complete()` (that is it is considered as an un-complete sentence because its first character is not a capital letter. How to improve on this ?
