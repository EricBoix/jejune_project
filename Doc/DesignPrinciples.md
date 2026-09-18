# Jejune Design Principles<!-- omit in toc -->

## Table of content<!-- omit in toc -->

- [Inter-Component UI Invocation](#inter-component-ui-invocation)
- [Document encoding](#document-encoding)
- [Concerning jejune\_cli](#concerning-jejune_cli)

## Inter-Component UI Invocation

When one UI component needs to hand off control to another running component
(e.g. the docs-server landing page opening the kg-graph-viewer for a specific
turtle file), the pattern used is **deep linking via query parameters**:

1. The source component renders an `<a target="_blank">` whose `href` points at
   the target component's URL with arguments encoded in the query string.
2. The browser opens the target in a new tab; no JavaScript event handler is
   needed on the source side.
3. The target component reads `window.location.search` with `URLSearchParams`
   on startup and initialises itself from the extracted values.

Arguments that are themselves URLs must be percent-encoded
(`encodeURIComponent`) so they survive embedding inside another URL.

This pattern requires no shared memory, no message-passing API, and no
coupling beyond the agreed query-parameter contract between the two components.

## Document encoding

### Markdown

- Original Markdown specification documents (like [those on Daring Fireball](https://daringfireball.net/projects/markdown/syntax)) do not strictly enforce a single character set.
- modern specifications like [GitHub Flavored Markdown](https://github.github.com/gfm/#preliminaries) state that "a character is a Unicode code point".

### JSON

JSON exchange in an open ecosystem [must be encoded in UTF-8](https://en.wikipedia.org/wiki/JSON#Character_encoding).

### YAML

YAML accepts the entire Unicode character set [...] and may be encoded in any one of UTF-8, UTF-16 or UTF-32.

### Jejune pipeline constraints

Some steps of the Jejune [RAG](https://en.wikipedia.org/wiki/Retrieval-augmented_generation) pipeline are sensitive/fragile to "smart quotes vs straight quotes" inconsistencies. For example the steps that require

- doing exact-match string operations e.g. to retrieve a quote/chunk in the original document,
- avoid tokens/embeddings fragmentation of what should be identical (near-duplicate) text,
- using regex e.g. in order to retrieve the structural elements of the original pdf document like chapters, sub-chapters...,
- ["deduplication"](https://en.wikipedia.org/wiki/Data_deduplication) e.g. of knowledge graph nodes coming from different sources (some chunks have curly quotes, some have straight quotes, depending on source document),
- embedding the markdown conversion into quote-sensitive document e.g. re-inserting markdown chunks into JSON/YAML

The general advice in such an operational context is to **fold U+2018/U+201 to ASCII '. The main reason being that "smart/curly quotes vs straight quotes" inconsistencies are more painful problem than losing typographic fidelity.

### Conclusion

Jejune relies on [UTF-8 (Unicode Transformation Format – 8-bit)](https://en.wikipedia.org/wiki/UTF-8) for the markdown encoding 
with a the following ASCII fold
  
   ```python
   QUOTE_MAP = {
         "\u2018": "'", "\u2019": "'",   # ' '
         "\u201C": '"', "\u201D": '"',   # " "
         "\u2032": "'", "\u2033": '"',   # primes
      }
   ```

   that must be consistently applied (for all documents and at all pipeline stages)

## Concerning jejune\_cli

Refer [jejune_cli documentation](https://github.com:EricBoix/jejune_project.git).
