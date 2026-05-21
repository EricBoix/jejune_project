# It focuses on providing a (hopefully) more refined breakdown of the
# original document than the one offered by langchain's
# RecursiveCharacterTextSplitter algorithm.
# Note: this code is derived from
#   https://github.com/Coding-Crashkurse/GraphRAG-with-Llama-3.1.git
import argparse
import json
import os
import sys

from langchain_text_splitters import MarkdownTextSplitter
from langchain_core.documents import Document
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
        "--load_json_document",
        type=str,
        metavar="JSON_FILE",
        help="Load documents from a JSON file instead of parsing markdown.",
    )
    parser.add_argument(
        "--load_markdown_document",
        type=str,
        metavar="MARKDOWN_FILE",
        help="Load documents from a markdown file.",
    )
    args = parser.parse_args()

    if args.load_json_document:
        if args.input_directory:
            args.json_file_path = os.path.join(
                args.input_directory, args.load_json_document
            )
        else:
            args.json_file_path = args.load_json_document

    if args.load_markdown_document:
        if args.input_directory:
            args.markdown_file_path = os.path.join(
                args.input_directory, args.load_markdown_document
            )
        else:
            args.markdown_file_path = args.load_markdown_document

    return args


def load_documents_from_json(json_path):
    def as_document(dct):
        if "__document__" in dct:
            return Document(metadata=dct["metadata"], page_content=dct["page_content"])
        return dct

    with open(json_path, "r") as in_file:
        try:
            documents = json.load(fp=in_file, object_hook=as_document)
        except ValueError as e:
            print(DEBUG_PROMPT, "Invalid json: %s" % e)
            sys.exit()
    return documents


def load_documents_from_markdown(file_path):
    loader = UnstructuredMarkdownLoader(file_path=file_path)
    docs = loader.load()
    text_splitter = MarkdownTextSplitter()
    documents = text_splitter.split_documents(documents=docs)
    return documents


def load_documents(args):
    documents = []  # The breakdown elements for LLMGraphTransformer algorithm
    if hasattr(args, "json_file_path"):
        documents.extend(load_documents_from_json(args.json_file_path))
    if hasattr(args, "markdown_file_path"):
        documents.extend(load_documents_from_markdown(args.markdown_file_path))
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
