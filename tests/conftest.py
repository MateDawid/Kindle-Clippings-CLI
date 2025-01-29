import shutil
from typing import Any

import pytest
from _pytest.fixtures import SubRequest


@pytest.fixture(scope="session", autouse=True)
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


@pytest.fixture
def clippings_list() -> list[dict[str, Any]]:
    """
    Example clippings for test purposes.

    Returns:
        list[dict[str, Any]]: Clippings list.
    """
    return [
        {
            "book": {"title": "Book 1", "author": "Author 1"},
            "content": "Content 1",
            "page_number": "1",
            "location": "123",
            "created_at": "2025-01-01",
            "clipping_type": "Highlight",
            "errors": {},
        },
        {
            "book": {"title": "Book 2", "author": "Author 2"},
            "content": "Content 2",
            "page_number": "2",
            "location": "456",
            "created_at": "2025-01-02",
            "clipping_type": "Note",
            "errors": {},
        },
    ]
