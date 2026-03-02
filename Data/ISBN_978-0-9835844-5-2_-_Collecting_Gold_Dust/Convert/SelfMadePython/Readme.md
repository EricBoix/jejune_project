# Extracting the book semantic structure out of Collecting Gold Dust book<!-- omit from toc -->

## Table of contents<!-- omit from toc -->

- [Introduction](#introduction)
- [Running things](#running-things)
- [Testing](#testing)

## Introduction

This directory holds a [copy of the pdf version of Sayadaw U Tejaniya's book
COLLECTING GOLD DUST Nurturing the Dhamma in Daily Living](./original_data/2019_-_Sayadaw-U-Tejaniya-Collecting-Gold-Dust-Web-Book-1.pdf) as offered e.g. by [this Scribd link](https://www.scribd.com/document/716383730/Collecting-Gold-Dust-Web-Book-1)

## Running things

```bash
cd `git rev-parse --show-toplevel`/Data/ISBN_978-0-9835844-5-2_-_Collecting_Gold_Dust/Convert/SelfMadePython
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
