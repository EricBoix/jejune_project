# Testing the handling of citations/references

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python bibtex.py
```

which illustrates how the [Citation Style Language (CSL)](https://citationstyles.org/) can be used in Python in order to separate the BibTeX library description from its presentation/usage.

The next step consists in introducing a component that takes a citation and

1. displays it properly as text with some chosen CSL style
2. enables an UI to retrieve the referenced document (when available) and display it

## References

- [citeproc-py Python package](https://github.com/citeproc-py/citeproc-py)
- [Citation Style Language (CSL)](https://citationstyles.org/) 
- [Academic markdown and citations](https://v4.chriskrycho.com/2015/academic-markdown-and-citations.html): couldn't get `pandoc` to make usage of the bibtex file.
  The following was tried:

  ```bash
  brew install pandoc
  pandoc -f markdown -t markdown test.md --bibliography library.bib  -o result.md
  ```
