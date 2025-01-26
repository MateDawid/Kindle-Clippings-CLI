import pytest
from clippings_cli.clippings_service.parsers import parse_book_line


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
        THEN: Book line parsed properly, function result the same as expected.
        """
        result = parse_book_line(line)
        assert result == expected_output
