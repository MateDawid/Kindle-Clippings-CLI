import shutil

import pytest
from _pytest.fixtures import SubRequest


@pytest.fixture
def cleanup_temp_files(request: SubRequest):
    """
    Fixture to clean up temporary files directory created during performing tests.

    Args:
        request (SubRequest): Test request.
    """

    def remove_temp_files():
        temp_dir = request.config._tmpdirhandler.getbasetemp()
        shutil.rmtree(temp_dir, ignore_errors=True)

    request.addfinalizer(remove_temp_files)
