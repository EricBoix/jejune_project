.PHONY: test clean setup clean-test

PYTHON := python3.10
VENV := venv

setup:
	$(PYTHON) -m venv $(VENV)
	source ./$(VENV)/bin/activate && pip install -r requirements.txt

clean:
	rm -rf $(VENV) __pycache__ .pytest_cache
	find . -type d -name '__pycache__' -not -path './*/venv/*' -exec rm -rf {} + 2>/dev/null || true

