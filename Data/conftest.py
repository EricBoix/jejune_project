import sys
from pathlib import Path

import pytest

DATA_DIR = Path(__file__).parent


@pytest.hookimpl(tryfirst=True)
def pytest_runtest_setup(item):
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
