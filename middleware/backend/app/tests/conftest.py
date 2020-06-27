import os
import pytest


@pytest.fixture(scope="function", autouse=True)
def scope_function(tmpdir):
    # Pre-processing
    os.chdir(tmpdir)
    yield
    # Post-processing
