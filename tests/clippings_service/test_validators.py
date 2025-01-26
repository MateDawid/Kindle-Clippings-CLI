import pytest
from clippings_cli.clippings_service.validators import validate_fields


class TestClippingServiceValidators:
    """
    Tests for clippings_service.validators.py.
    """

    @pytest.mark.parametrize(
        "clipping",
        (
            pytest.param(
                {
                    "book": {"title": "Title", "author": "Author"},
                    "clipping_type": "Highlight",
                    "page_number": 1,
                    "created_at": "2025-01-01 18:00:00",
                    "location": 1,
                    "content": "Content",
                },
                id="valid-clipping",
            ),
            pytest.param(
                {
                    "book": {"title": "Title", "author": "Author"},
                    "clipping_type": "Highlight",
                    "page_number": 1,
                    "created_at": "2025-01-01 18:00:00",
                    "location": 1,
                    "content": "Content",
                    "additional_key": "Additional",
                },
                id="additional-data",
            ),
        ),
    )
    def test_clipping_valid(self, clipping: dict):
        """
        GIVEN: Dictionary with valid Clipping data.
        WHEN: Executing validate_fields on clipping dict.
        THEN: No errors in result.
        """
        result = validate_fields(clipping=clipping)
        assert result == {}

    @pytest.mark.parametrize(
        "clipping",
        (
            pytest.param({}, id="empty"),
            pytest.param({"additional": True}, id="other-keys"),
            pytest.param(
                {
                    "clipping_type": "Highlight",
                    "page_number": 1,
                    "created_at": "2025-01-01 18:00:00",
                    "location": 1,
                    "content": "Content",
                },
                id="book-missing",
            ),
            pytest.param(
                {
                    "book": {"title": "Title", "author": "Author"},
                    "page_number": 1,
                    "created_at": "2025-01-01 18:00:00",
                    "location": 1,
                    "content": "Content",
                },
                id="clipping-type-missing",
            ),
            pytest.param(
                {
                    "book": {"title": "Title", "author": "Author"},
                    "clipping_type": "Highlight",
                    "created_at": "2025-01-01 18:00:00",
                    "location": 1,
                    "content": "Content",
                },
                id="created-at-missing",
            ),
            pytest.param(
                {
                    "book": {"title": "Title", "author": "Author"},
                    "clipping_type": "Highlight",
                    "page_number": 1,
                    "created_at": "2025-01-01 18:00:00",
                    "content": "Content",
                },
                id="location-missing",
            ),
            pytest.param(
                {
                    "book": {"title": "Title", "author": "Author"},
                    "clipping_type": "Highlight",
                    "page_number": 1,
                    "created_at": "2025-01-01 18:00:00",
                    "location": 1,
                },
                id="content-missing",
            ),
        ),
    )
    def test_clipping_invalid(self, clipping: dict):
        """
        GIVEN: Dictionary with invalid Clipping data.
        WHEN: Executing validate_fields on clipping dict.
        THEN: Errors about missing fields in result.
        """
        result = validate_fields(clipping=clipping)
        assert result != {}
        for key in result.keys():
            assert result[key] == f"Field {key} missed in Clipping."
