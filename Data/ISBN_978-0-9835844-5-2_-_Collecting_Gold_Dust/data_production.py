# Producing the content of result_data directory
import pathlib
import os
import sys
import subprocess
import shutil

if __name__ == "__main__":
    this_script_dir = pathlib.Path(__file__).parent.resolve()
    converter_dir = os.path.join(this_script_dir, "Convert/SelfMadePython")
    venv_python_bin = os.path.join(converter_dir, "venv/bin/python")

    if not os.path.exists(venv_python_bin):
        print(
            f"Virtual environment python interpreter ({venv_python_bin}) not found. Exiting."
        )
        sys.exit()
    convert_script_file = os.path.join(converter_dir, "main.py")

    if not os.path.exists(convert_script_file):
        print(f"Converter script ({convert_script_file}) not found. Exiting.")
        sys.exit()

    subprocess.Popen([venv_python_bin, convert_script_file])

    # Renaming and moving relevant outputs
    output_dir = os.path.join(this_script_dir, "result_data")
    converted_markdown_source = os.path.join(converter_dir, "output.md")

    if not os.path.exists(converted_markdown_source):
        print(
            f"Converted markdown output file ({converted_markdown_source}) not found. Exiting."
        )
        sys.exit()

    converted_markdown_target = os.path.join(
        output_dir,
        "2019_-_Sayadaw-U-Tejaniya-Collecting-Gold-Dust-Web-Book-1_-_local_converter.md",
    )
    shutil.copy(converted_markdown_source, converted_markdown_target)
    sentences_source = os.path.join(
        converter_dir, "Sentences_as_LangChain_Document.json"
    )
    if not os.path.exists(sentences_source):
        print(f"Sentences output file ({sentences_source}) not found. Exiting.")
        sys.exit()
    sentences_target = os.path.join(
        output_dir,
        "2019_-_Sayadaw-U-Tejaniya-Collecting-Gold-Dust-Web-Book-1_-_Sentences_as_LangChain_Document.json",
    )
    shutil.copy(sentences_source, sentences_target)
    print("Following files created/overwritten to output:")
    print(f"  - {converted_markdown_target}")
    print(f"  - {sentences_target}")
