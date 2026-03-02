# Extracting the book semantic structure out of Collecting Gold Dust book<!-- omit from toc -->

## Table of contents<!-- omit from toc -->

- [Introduction](#introduction)
- [Running things](#running-things)
- [Testing](#testing)

## Introduction

This directory holds a a modified copy of the Python code used to convert Collecting Gold Dust.
Refer to the [original directory for design notes](../../../ISBN_978-0-9835844-5-2_-_Collecting_Gold_Dust/Readme.md#extracting-the-book-semantic-structure-out-of-collecting-gold-dust-book)...

## Running things

```bash
cd `git rev-parse --show-toplevel`/Data/ISBN_978-1-5011-5698-4_-_The_Mind_Illuminated/Convert/SelfMadePython
python3.10 -m venv venv
source ./venv/bin/activate
pip install -r ../../../requirements.txt
python main.py
```

## Testing

Within the above running context (directory and installed virtual environment)

```bash
pytest test_main.py
```
