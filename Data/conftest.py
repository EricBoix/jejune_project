import sys
from pathlib import Path

import pytest

DATA_DIR = Path(__file__).parent
SHARED_MODULES_DIR = str(DATA_DIR / "ConvertPdfToMarkdown")


@pytest.hookimpl(tryfirst=True)
def pytest_runtest_setup(item):
    test_dir = str(Path(item.fspath).parent)
    if test_dir not in sys.path:
        sys.path.insert(0, test_dir)
    if SHARED_MODULES_DIR not in sys.path:
        sys.path.insert(0, SHARED_MODULES_DIR)


@pytest.hookimpl(trylast=True)
def pytest_runtest_teardown(item, nextitem):
    test_dir = str(Path(item.fspath).parent)
    if test_dir in sys.path:
        sys.path.remove(test_dir)
    if SHARED_MODULES_DIR in sys.path:
        sys.path.remove(SHARED_MODULES_DIR)
