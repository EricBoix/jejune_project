# Extracting the book semantic structure out of Collecting Gold Dust book<!-- omit from toc -->

## Table of contents<!-- omit from toc -->

- [Introduction](#introduction)
- [Running things](#running-things)
- [Requirements and known difficulties](#requirements-and-known-difficulties)
- [Model class diagram](#model-class-diagram)
- [References How to recover document structure and plain text from PDF?](#references-how-to-recover-document-structure-and-plain-text-from-pdf)
- [References Converting PDF to markdown techniques](#references-converting-pdf-to-markdown-techniques)

## Introduction

This directory holds a [copy of the pdf version of Sayadaw U Tejaniya's book
COLLECTING GOLD DUST Nurturing the Dhamma in Daily Living](./original_data/2019_-_Sayadaw-U-Tejaniya-Collecting-Gold-Dust-Web-Book-1.pdf) as offered e.g. by [this Scribd link](https://www.scribd.com/document/716383730/Collecting-Gold-Dust-Web-Book-1) 

## Running things

```bash
python3.10 -m venv venv
source ./venv/bin/activate
pip install -r requirements.txt
python main.py
```

## Requirements and known difficulties

### Need: division references at the sentence level

Assume we have a text document (or work) that we wish to annotate with references to external documents. Later on we will use a document browser that proposes some visual clues about the existing annotations and offers some technical means to access them. The classic illustrations are e.g. underlined URL links within html or tooltip popups (think of Wikipedia browsing).
Additionally, we wish such annotations to be at the sentence level (because, most often, this is the semantic atomic level).
In order to be able to refer to part of another document (work, book...textual document) and without quoting that document (that is copy the part of interest of the other document within the current document) we thus need a `sentence reference`.
A `sentence reference` is a concrete mean to designate a single sentence within a text document.

Note that short (or even long) quotations usually don't offer a sentence level reference but only a page reference (refer e.g. to the [OWL's in-text citation guide](https://owl.purdue.edu/owl/research_and_citation/apa_style/apa_formatting_and_style_guide/in_text_citations_the_basics.html), [Monash's citing and referencing](https://guides.lib.monash.edu/citing-referencing/vancouver-intext)) when [Harvard's referencing guide](https://libguides.scu.edu.au/harvard/citing-in-text) limit's itself to referencing the document as a whole.

The [bible citation](https://en.wikipedia.org/wiki/Bible_citation) is a bit more precise reference that is only possible because the original text publishers offer (diverse) multi-level referenceable divisions like [chapters](https://en.wikipedia.org/wiki/Chapters_and_verses_of_the_Bible#Chapters), section, paragraphs, [verses](https://en.wikipedia.org/wiki/Chapters_and_verses_of_the_Bible#Verses) and phrases.
Alas verse divisions are quite arbitrary (and thus not unique) and we should prefer a standardized multi-level division system.
Although as the one proposing such division (and in order to avoid any ambiguity or even mistake due to some failing division algorithm) we should provide the divided version of the original texts.
As `dividers` we should provide the texts with the inclusion/integration within those texts of the build/computed division/references (in a fashion similar to the one used by [Robert Etienne](https://en.wikipedia.org/wiki/Chapters_and_verses_of_the_Bible) we he introduced is verse numbering).

A `division reference` could look like **"chapter 3, sub-chapter I, paragraph 2, sentence 4"** of `document reference` "author_A, author_B book titled book_title, ISBN".

If we adopt such division based referencing, we should not only provide the resulting divisions (and division references) but also the algorithms producing such divisions.

#### Concerning page numbering

A `division reference` should be intrinsic to the document content (the text) as opposed to extrinsic that is referring to a particular layout or printing format (that depends the chosen layout that in turns depends on the paper size and the font).
The intrinsic property of a `division reference` prevents the usage of page numbering.
Nevertheless, when the original document (E-books in pdf or an [OCRized](https://en.wikipedia.org/wiki/Optical_character_recognition) version of a paper form) did provide some page numbering a division reference might chose to provide a page number as long as the exact source document is cited (provide an ISBN or a specific edition number).

Note that for some E-books that distributed in pdf do not provide page numbering.
Still, because pdf can be seen as a set of pages (look for `pages tree` in pdf document), when interpreted a pdf document will emit pages (which does not imply that the document rendered with a pdf viewer will display page numbers). When possible such "renderer page number" might be used to decorate the `division reference` and the pdf should be provided.

Also note that the pdf rendering of scanned/ocrized paper books (or of an electronic version of a book that is also distributed in paper form) is (usually) page based and on many such pages a number is displayed (the numbering is here part of the content of the document). Sometimes such numbering does not start at page one, but might have prologues (or introductory notes) that have a roman numbering before starting a new digit based page numbering at the end of that section (in which case you might have a page `iii` and later on a page `3`). Besides such page numberings are usually different from the pdf page numbers (that is the page number obtained once the pdf layout is rendered by some viewer). For example the cover of a book (for the printed copy or when rendered with a pdf viewer) does not show any page number. Yet the pdf viewer does show a page number (not in the text section but in the layout section of the pdf viewer).
In which case a `division reference` that is decorated with a page number should use the content page number (that is the page number that is included in the content of the document and shown in the paper copy).

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

## References How to recover document structure and plain text from PDF?

- Reddit post on [How to recover document structure and plain text from PDF?](https://www.reddit.com/r/LocalLLaMA/comments/1am3fz8/how_to_recover_document_structure_and_plain_text) with a focus on RAG applications.
- PDFMiner.six [explanations of how difficult extracting text from pdf can be](https://pdfminersix.readthedocs.io/en/latest/topic/converting_pdf_to_text.html)

## References Converting PDF to markdown techniques

https://medium.com/data-science-collective/convert-pdfs-to-markdown-using-local-llms-c5232f3b50fc
