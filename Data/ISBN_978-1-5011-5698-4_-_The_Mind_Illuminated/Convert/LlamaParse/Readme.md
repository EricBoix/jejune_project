# Converting from pdf through usage of non-free Llamaparse

We here follow the [Llamaparse introductory documentation](https://www.llamaindex.ai/blog/pdf-parsing-llamaparse)

- create an account on cloud.llamaparse.ai

- ```bash
  python3.10 -m venv venv
  source ./venv/bin/activate
  pip install -r requirements.txt
  python main_llama_parse.py
  ```

- ```bash
  mkdir result_data
  cd result_data
  # Store the original result
  cp ../output.md 2017_-_Culadasa_John_Yates-Matthew_Immergut-Jeremy_Graves_-_The_Mind_Illuminated_-_llamaparse_raw_conversion.md
  # Manually modify the result
  cp ../output.md 2017_-_Culadasa_John_Yates-Matthew_Immergut-Jeremy_Graves_-_The_Mind_Illuminated_-_llamaparse_manually_fixed.md
  ```

- Proceed with manually correcting the Llama_parse flawed output.
