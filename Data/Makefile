.PHONY: test clean setup clean-test

PYTHON := python3.10
VENV := venv

test:
	source ./$(VENV)/bin/activate && pytest

setup:
	$(PYTHON) -m venv $(VENV)
	source ./$(VENV)/bin/activate && pip install -r requirements.txt
	source ./$(VENV)/bin/activate && pip install git+https://github.com/EricBoix/pdf-to-markdown.git
	@if [ -d "ISBN_978-0-9835844-5-2_-_Collecting_Gold_Dust" ]; then \
		git -C ISBN_978-0-9835844-5-2_-_Collecting_Gold_Dust pull; \
	else \
		git clone https://github.com/EricBoix/jj_doc_Collecting_Gold_Dust.git ISBN_978-0-9835844-5-2_-_Collecting_Gold_Dust; \
	fi

clean:
	rm -rf $(VENV) __pycache__ .pytest_cache
	find . -type d -name '__pycache__' -not -path './*/venv/*' -exec rm -rf {} + 2>/dev/null || true

clean-test: clean setup test
