# Data Directory<!-- omit from toc -->

## Table of contents<!-- omit from toc -->

- [Setup](#setup)
- [Running tests](#running-tests)
- [Model class diagram](#model-class-diagram)
- [References](#references)

## Setup

```bash
cd Data
python3.10 -m venv venv
source ./venv/bin/activate
pip install -r requirements.txt
```

## Running tests

```bash
cd Data
source ./venv/bin/activate
pytest                    # all tests
pytest -v                 # verbose
pytest ISBN_978-...       # specific book directory
```

## Model class diagram

```mermaid
classDiagram
  namespace SemanticDocument {
    class Document {
    }

    class Chapter {
    }
    class Paragraph {

    }

    class Sentence {
    }
  }

  Document *-- Chapter
  Chapter *-- Paragraph
  Chapter <-- Paragraph
  Paragraph *-- Sentence
  Paragraph <-- Sentence

  namespace pypdf {
    class Reader {
    }
    class Page {
    }
  }
  Reader *-- Page

  namespace Conversion {
    class Converter{
    }
    class ExtractedPage {
    }
    class PageLayout {
    int page # Starts on that page
  }
  }
  Chapter o-- PageLayout
  Paragraph o-- PageLayout
  Sentence o-- PageLayout

  Converter *-- ExtractedPage
  Chapter o-- ExtractedPage
  ExtractedPage --> Page

```

## References

### Recovering document structure from PDF

- Reddit post on [How to recover document structure and plain text from PDF?](https://www.reddit.com/r/LocalLLaMA/comments/1am3fz8/how_to_recover_document_structure_and_plain_text) with a focus on RAG applications.
- PDFMiner.six [explanations of how difficult extracting text from pdf can be](https://pdfminersix.readthedocs.io/en/latest/topic/converting_pdf_to_text.html)

### Converting PDF to markdown

<https://medium.com/data-science-collective/convert-pdfs-to-markdown-using-local-llms-c5232f3b50fc>
