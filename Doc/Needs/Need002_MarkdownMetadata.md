# Need 002: embedding metadata in a Markdown format

Things boil down to this [StackOverflow](https://stackoverflow.com/questions/44215896/markdown-metadata-format) question:

```text
Is there a standard or convention for embedding metadata in a Markdown formatted post, such as the publication date or post author for conditional rendering by the renderer? Looks like this Yaml metadata format might be it.
```

Note:

- vscode markdown renderer seems to support Yaml metadata. This can be combined
with standard markdown syntax like link references e.g.

```text
---
[_metadata_:author]:- "daveying"
[_metadata_:tags]:- "markdown metadata"
---

# The markdown title
```

so that other markdown parsers can work on the data !?
