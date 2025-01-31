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
def clippings_input() -> str:
    """
    Example clippings input file content containing 3 Clippings.

    Returns:
        str: Clippings file content.
    """
    return """Book 1 (Author 1)
- Your Highlight on page 1 | location 11-12 | Added on Sunday, 1 January 2025 05:00:00

Highlighted content.
==========
Book 2 (Author 2)
- Your Note on page 2 | location 11-12 | Added on Sunday, 1 January 2025 06:00:00

Noted content.
==========
Book 3 (Author 3)
- Your Highlight on page 3 | location 11-12 | Added on Sunday, 1 January 2025 07:00:00

Highlighted content.
=========="""


@pytest.fixture
def clippings_list() -> list[dict[str, Any]]:
    """
    Example Clippings list. Equal to parsed clippings_input fixture Clippings.

    Returns:
        list[dict[str, Any]]: Clippings list.
    """
    return [
        {
            "book": {"title": "Book 1", "author": "Author 1"},
            "clipping_type": "Highlight",
            "page_number": "1",
            "location": "11-12",
            "created_at": "2025-01-01 05:00:00",
            "content": "Highlighted content.",
            "errors": {},
        },
        {
            "book": {"title": "Book 2", "author": "Author 2"},
            "clipping_type": "Note",
            "page_number": "2",
            "location": "11-12",
            "created_at": "2025-01-01 06:00:00",
            "content": "Noted content.",
            "errors": {},
        },
        {
            "book": {"title": "Book 3", "author": "Author 3"},
            "clipping_type": "Highlight",
            "page_number": "3",
            "location": "11-12",
            "created_at": "2025-01-01 07:00:00",
            "content": "Highlighted content.",
            "errors": {},
        },
    ]
