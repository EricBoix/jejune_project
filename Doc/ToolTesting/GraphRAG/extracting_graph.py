# Uses langchain's RecursiveCharacterTextSplitter for document breakdown.
# Note: this code is derived from
#   https://github.com/Coding-Crashkurse/GraphRAG-with-Llama-3.1.git
import argparse
import os
import sys

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import UnstructuredMarkdownLoader

from graph_utils import (
    DEBUG_PROMPT,
    create_neo4j_database,
    extract_graph,
    initialize_llm,
)


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Extract graph from documents using LLM and store in Neo4j."
    )
    parser.add_argument(
        "--input_directory",
        type=str,
        metavar="DIR",
        help="Directory to prefix to all loaded file paths.",
    )
    parser.add_argument(
        "--load_markdown_document",
        type=str,
        metavar="MARKDOWN_FILE",
        help="Load documents from a markdown file.",
    )
    parser.add_argument(
        "--chunk_size",
        type=int,
        default=250,
        metavar="SIZE",
        help="Chunk size for text splitting (default: 250).",
    )
    parser.add_argument(
        "--chunk_overlap",
        type=int,
        default=24,
        metavar="OVERLAP",
        help="Chunk overlap for text splitting (default: 24).",
    )
    args = parser.parse_args()

    if args.load_markdown_document:
        if args.input_directory:
            args.markdown_file_path = os.path.join(
                args.input_directory, args.load_markdown_document
            )
        else:
            args.markdown_file_path = args.load_markdown_document

    return args


def load_documents_from_markdown(file_path, chunk_size=250, chunk_overlap=24):
    loader = UnstructuredMarkdownLoader(file_path=file_path)
    docs = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )
    documents = text_splitter.split_documents(documents=docs)
    return documents


def load_documents(args):
    documents = []
    if hasattr(args, "markdown_file_path"):
        documents.extend(
            load_documents_from_markdown(
                args.markdown_file_path, args.chunk_size, args.chunk_overlap
            )
        )
    if not documents:
        print(DEBUG_PROMPT + "No documents loaded. Exiting.")
        sys.exit()
    else:
        print(
            DEBUG_PROMPT + "Number of documents for LLMGraphTransformer to deal with: ",
            len(documents),
        )
    return documents


def main():
    args = parse_arguments()
    documents = load_documents(args)
    llm = initialize_llm()
    graph_documents = extract_graph(llm, documents)
    create_neo4j_database(graph_documents)


if __name__ == "__main__":
    main()
