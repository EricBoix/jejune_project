import sys
import json
from .Model import (
    TopLevelChapterOfParagraphs,
    SubChapterOfParagraphs,
    Paragraph,
    Sentence,
)

# Warning: implicit dependency towards LangChain's Document class


class LangChainDocumentEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Sentence):
            return {
                "__document__": True,
                "metadata": {"source": obj.get_document_reference_long()},
                "page_content": obj.text,
            }
        # Let the base class default method raise the TypeError
        return super().default(obj)


class WriteAsLangchainDocuments:
    """
    Export the ConvertPdfToMarkdown Document transposed to Langchain's Document objects and into JSON based files
    References: https://reference.langchain.com/python/langchain-core/documents/base/Document
    """

    def __init__(self, document):
        self._document = document

    def _collect_level_sentences(self, level, output_json_file):
        collected_sentences = []
        for sublevel in level.get_sublevels():
            if isinstance(sublevel, Paragraph):
                sentences = sublevel.get_sentences()
                if not sentences:
                    continue
                for sentence in sentences:
                    collected_sentences.append(sentence)
                continue
            elif isinstance(
                sublevel, (TopLevelChapterOfParagraphs, SubChapterOfParagraphs)
            ):
                collected_sentences.extend(
                    self._collect_level_sentences(sublevel, output_json_file)
                )
                continue
            else:
                print("Level ", sublevel, "not serializable as sentences ???")
                print("Exiting.")
                sys.exit()
        return collected_sentences

    def write_sentences(self, output_json_filename):
        with open(output_json_filename, "w+") as output_json_file:
            # output_json_file.write("[")
            collected_sentences = []
            for chapter in self._document.get_chapters():
                collected_sentences.extend(
                    self._collect_level_sentences(chapter, output_json_file)
                )
            json.dump(
                collected_sentences,
                cls=LangChainDocumentEncoder,
                fp=output_json_file,
                indent=4,
            )
            # output_json_file.write("]")

            #                 json.dump(
            #             sentence,
            #             cls=LangChainDocumentEncoder,
            #             fp=output_json_file,
            #             indent=4,
            #         )
