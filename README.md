# jejuneness

Don't let the [monkey](https://en.wikipedia.org/wiki/Monkey_mind) prevent you from sitting back on the [cushion](https://en.wikipedia.org/wiki/Zafu).

## What's next

### Semantic Chunking

The [`ToolTesting/GraphRAG/extracting_graph.py` code](./Doc/ToolTesting/GraphRAG/extracting_graph.py#32) currently uses [LangChain's `RecursiveCharacterTextSplitter`](https://reference.langchain.com/python/langchain-text-splitters/character/RecursiveCharacterTextSplitter) as "chunker". But knowledge graph focuses on semantics and using a semantic based chunker can only improve things (although it comes at a cost) at two levels : retrieval and citation. Since the [`ConvertPdfToMarkdown` package] produces sentence (and/or paragraph, sub-section...) based outputs we have the natural opportunity to use the available semantic chunkers starting with [lanchain_exprimental's  `SemanticChunker`](https://github.com/langchain-ai/langchain-experimental/blob/main/libs/experimental/langchain_experimental/text_splitter.py#L99).

References:

- [`SemanticChunker` class](https://github.com/langchain-ai/langchain-experimental/blob/main/libs/experimental/langchain_experimental/text_splitter.py#L99) as offered by [lanchain_exprimental (python package)](https://github.com/langchain-ai/langchain-experimental/tree/main)
- [langchain_experimental "SemanticChunker" tutorial](https://colab.research.google.com/github/LangChain-OpenTutorial/LangChain-OpenTutorial/blob/main/07-TextSplitter/04-SemanticChunker.ipynb#scrollTo=312e3aae)
- ["A Visual Exploration of Semantic Text Chunking" article](https://towardsdatascience.com/a-visual-exploration-of-semantic-text-chunking-6bb46f728e30/):
  - :warning: This article mentions that it is key to "use a model that has been trained to generate meaningful embeddings" and forwards to [`SentenceTransformers` library](https://sbert.net/)
- [Langchain's tutorial: Build a semantic search engine with LangChain](https://docs.langchain.com/oss/python/langchain/knowledge-base)
