import sys
from pathlib import Path

import pytest

DATA_DIR = Path(__file__).parent

# Module names that are defined locally in each test directory
# and must be reimported fresh for each test
LOCAL_MODULE_NAMES = {"Converter", "ExtractedPage", "StructuralInfo"}

# Prefixes of modules that should be cleared to prevent cross-test pollution
POLLUTING_MODULE_PREFIXES = (
    "Converter",
    "ExtractedPage",
    "StructuralInfo",
    "ConvertPdfToMarkdown",
    "pypdf",
)


@pytest.hookimpl(tryfirst=True)
def pytest_runtest_setup(item):
    # Aggressively clear all potentially polluting modules
    modules_to_clear = [
        name for name in list(sys.modules.keys())
        if name.startswith(POLLUTING_MODULE_PREFIXES) or name in LOCAL_MODULE_NAMES
    ]
    for mod_name in modules_to_clear:
        del sys.modules[mod_name]

    test_dir = str(Path(item.fspath).parent)
    if test_dir not in sys.path:
        sys.path.insert(0, test_dir)


@pytest.hookimpl(trylast=True)
def pytest_runtest_teardown(item, nextitem):
    test_dir = str(Path(item.fspath).parent)
    if test_dir in sys.path:
        sys.path.remove(test_dir)
    # Clear cached modules from test directory to prevent cross-test pollution
    modules_to_remove = [
        name
        for name, module in sys.modules.items()
        if hasattr(module, "__file__")
        and module.__file__
        and module.__file__.startswith(test_dir)
    ]
    for name in modules_to_remove:
        del sys.modules[name]
