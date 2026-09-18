# Jejune Design Principles<!-- omit in toc -->

## Table of content<!-- omit in toc -->

- [Inter-Component UI Invocation](#inter-component-ui-invocation)
- [Document encoding](#document-encoding)
  - [Markdown](#markdown)
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

Jejune relies on [UTF-8 (Unicode Transformation Format – 8-bit)](https://en.wikipedia.org/wiki/UTF-8) for the markdown encoding.

## Concerning jejune\_cli

Refer [jejune_cli documentation](https://github.com:EricBoix/jejune_project.git).
