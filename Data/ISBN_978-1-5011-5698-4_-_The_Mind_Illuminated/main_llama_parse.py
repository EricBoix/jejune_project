if __name__ == "__main__":

    import os
    import sys

    ### The following variables should work by default
    MODEL_ID = "featherless_ai/qwen2.5-coder:32b-instruct-fp16"
    OPENWEBUI_API_ENDPOINT = "ollama/v1/"
    # the API_KEY imported from the environment variable as follows
    try:
        LLAMAPARSE_API_KEY = os.environ["LLAMAPARSE_API_KEY"]
    except KeyError:
        print("LLAMA_ARSE_API_KEY environment variable was not set.")
        print("Exiting.")
        sys.exit(1)

    # The following code is a copy of the tutorial example found at
    # https://www.llamaindex.ai/blog/pdf-parsing-llamaparse
    from llama_parse import LlamaParse

    parser = LlamaParse(
        api_key=LLAMAPARSE_API_KEY,
        result_type="markdown",  # "markdown" and "text" are available,
        extract_charts=True,
        auto_mode=True,
        auto_mode_trigger_on_image_in_page=True,
        auto_mode_trigger_on_table_in_page=True,
    )

    file_name = "./original_data/2017_-_Culadasa_John_Yates-Matthew_Immergut-Jeremy_Graves_-_The_Mind_Illuminated.pdf"
    extra_info = {"file_name": file_name}

    with open(f"./{file_name}", "rb") as f:
        # must provide extra_info with file_name key with passing file object
        documents = parser.load_data(f, extra_info=extra_info)

    # with open('output.md', 'w') as f:
    # print(documents, file=f)

    # Write the output to a file
    with open("output.md", "w", encoding="utf-8") as f:
        for doc in documents:
            f.write(doc.text)
