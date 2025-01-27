import pytest
from clippings_cli.clippings_service.parsers import parse_book_line, parse_content_line, parse_metadata_line


class TestClippingServiceParsers:
    """
    Tests for clippings_service.parsers.py.
    """

    @pytest.mark.parametrize(
        "line, expected_output",
        (
            pytest.param(
                "Book title (Book Author)",
                {"book": {"title": "Book title", "author": "Book Author"}},
                id="with-parentheses-1",
            ),
            pytest.param(
                "Book title (For Book Readers) (Book Author)",
                {"book": {"title": "Book title (For Book Readers)", "author": "Book Author"}},
                id="with-parentheses-2",
            ),
            pytest.param(
                "Book title - Book Author", {"book": {"title": "Book title", "author": "Book Author"}}, id="with-dash-1"
            ),
            pytest.param(
                "Book title - Book Author-Bookowski",
                {"book": {"title": "Book title", "author": "Book Author-Bookowski"}},
                id="with-dash-2",
            ),
            pytest.param(
                "Book title - Booker", {"book": {"title": "Book title", "author": "Booker"}}, id="with-dash-3"
            ),
            pytest.param(
                "Book title - Part 2 - Book Author",
                {"book": {"title": "Book title - Part 2", "author": "Book Author"}},
                id="with-dash-4",
            ),
            pytest.param(
                "Book title - Part 2 - Book Author-Bookowski",
                {"book": {"title": "Book title - Part 2", "author": "Book Author-Bookowski"}},
                id="with-dash-5",
            ),
            pytest.param(
                "Book title - Part 2 - Booker",
                {"book": {"title": "Book title - Part 2", "author": "Booker"}},
                id="with-dash-6",
            ),
            pytest.param("Book title, Book Author", {}, id="not-supported"),
        ),
    )
    def test_parse_book_line(self, line: str, expected_output: dict):
        """
        GIVEN: Clipping line with Book details - title and author.
        WHEN: Calling parse_book_line with line as an argument.
        THEN: Line parsed properly, function result the same as expected.
        """
        result = parse_book_line(line)
        assert result == expected_output

    @pytest.mark.parametrize(
        "line, expected_output",
        (
            pytest.param(
                "- Your Highlight on page 14 | location 208 | Added on Tuesday, 26 July 2022 17:59:48",
                {
                    "clipping_type": "Highlight",
                    "page_number": "14",
                    "location": "208",
                    "created_at": "2022-07-26 17:59:48",
                },
                id="highlight",
            ),
            pytest.param(
                "- Your Note on page 14 | location 208 | Added on Tuesday, 26 July 2022 17:59:48",
                {"clipping_type": "Note", "page_number": "14", "location": "208", "created_at": "2022-07-26 17:59:48"},
                id="note",
            ),
            pytest.param(
                "- Your Highlight on page 14 | Added on Tuesday, 26 July 2022 17:59:48",
                {
                    "clipping_type": "Highlight",
                    "page_number": "14",
                    "location": None,
                    "created_at": "2022-07-26 17:59:48",
                },
                id="without-location",
            ),
            pytest.param(
                "- Your Highlight on page 14 | location 208-208 | Added on Tuesday, 26 July 2022 17:59:48",
                {
                    "clipping_type": "Highlight",
                    "page_number": "14",
                    "location": "208-208",
                    "created_at": "2022-07-26 17:59:48",
                },
                id="location-with-dash",
            ),
            pytest.param(
                "- Your Highlight on page 14-14 | location 208 | Added on Tuesday, 26 July 2022 17:59:48",
                {
                    "clipping_type": "Highlight",
                    "page_number": "14-14",
                    "location": "208",
                    "created_at": "2022-07-26 17:59:48",
                },
                id="page-with-dash",
            ),
        ),
    )
    def test_parse_metadata_line_with_page(self, line: str, expected_output: dict):
        """
        GIVEN: Clipping line with Clipping metadata - type, location, page_number, created_at
        matching METADATA_WITH_PAGE_REGEX.
        WHEN: Calling parse_metadata_line with line as an argument.
        THEN: Line parsed properly, function result the same as expected.
        """
        result = parse_metadata_line(line)
        assert result == expected_output

    @pytest.mark.parametrize(
        "line, expected_output",
        (
            pytest.param(
                "- Your Highlight at location 123 | Added on Tuesday, 11 July 2023 15:50:10",
                {
                    "clipping_type": "Highlight",
                    "page_number": None,
                    "location": "123",
                    "created_at": "2023-07-11 15:50:10",
                },
                id="highlight",
            ),
            pytest.param(
                "- Your Note at location 123 | Added on Tuesday, 11 July 2023 15:50:10",
                {"clipping_type": "Note", "page_number": None, "location": "123", "created_at": "2023-07-11 15:50:10"},
                id="note",
            ),
            pytest.param(
                "- Your Highlight at location 123-124 | Added on Tuesday, 11 July 2023 15:50:10",
                {
                    "clipping_type": "Highlight",
                    "page_number": None,
                    "location": "123-124",
                    "created_at": "2023-07-11 15:50:10",
                },
                id="location-with-dash",
            ),
        ),
    )
    def test_parse_metadata_line_without_page(self, line: str, expected_output: dict):
        """
        GIVEN: Clipping line with Clipping metadata - type, location, page_number, created_at
        matching METADATA_WITHOUT_PAGE_REGEX.
        WHEN: Calling parse_metadata_line with line as an argument.
        THEN: Line parsed properly, function result the same as expected.
        """
        result = parse_metadata_line(line)
        assert result == expected_output

    @pytest.mark.parametrize(
        "line, expected_output",
        (
            pytest.param("", "", id="empty-string"),
            pytest.param("\xa0", "", id=r"\xa0"),
            pytest.param("Clipping content!", "Clipping content!", id="regular-content"),
            pytest.param("\xa0Clipping\xa0content!\xa0", "Clipping content!", id=r"content-with-\xa0"),
        ),
    )
    def test_parse_content_line(self, line: str, expected_output: str):
        """
        GIVEN: Clipping line with Clipping content.
        WHEN: Calling parse_content_line with line as an argument.
        THEN: Line parsed properly, function result the same as expected.
        """
        result = parse_content_line(line)
        assert result["content"] == expected_output
