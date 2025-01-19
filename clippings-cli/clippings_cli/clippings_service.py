"""
Constants:
    BOOK_WITH_PARENTHESES_REGEX (str) - Regex to handle book title Clipping line, like "Book title (Book author)".
    BOOK_WITH_DASH_REGEX (str) - Regex to handle book title Clipping line, like "Book title - Book author".
    METADATA_WITH_PAGE_REGEX (str) - Regex to handle Clipping metadata line with page as first mentioned param, like
    "- Your Highlight on page 3 | location 41-41 | Added on Monday, 6 February 2023 06:32:11"
    METADATA_WITHOUT_PAGE_REGEX (str) - Regex to handle Clipping metadata line without page as first mentioned
    param, like "- Your Bookmark at location 579 | Added on Tuesday, 27 September 2022 15:45:30".
"""
import re
from collections import namedtuple
from datetime import datetime

BOOK_WITH_PARENTHESES_REGEX: str = r"^(.*) \((.*)\)$"
BOOK_WITH_DASH_REGEX: str = r"^(.*) - (.*)$"
METADATA_WITH_PAGE_REGEX: str = (
    r"^- Your (\w+) on page (\d+|\d+-\d+) \| (location (\d+|\d+-\d+) \| )?Added on (\w+), (.*)$"
)
METADATA_WITHOUT_PAGE_REGEX: str = r"^- Your (\w+) at location (\d+|\d+-\d+) \| Added on (\w+), (.*)$"


Book = namedtuple("Book", ["title", "author"])
Clipping = namedtuple(
    "Clipping", ["book", "clipping_type", "page_number", "created_at", "location", "content", "error"]
)


class ClippingsService:
    """
    Class for retrieving Clippings from input Clippings file.

    Args:
        path (str): Full path to Clippings file.

    Attributes:
        clippings (list[Clipping]): List of collected Clippings.

    """

    def __init__(self, path: str):
        self.path: str = path
        self.clippings: list[Clipping] = self._parse_clippings()

    def _parse_clippings(self) -> list[Clipping]:
        """
        Parses Clippings source file and stores them in list of Clipping namedtuple objects.

        Example clipping:
        [Line 0] Django for APIs (William S. Vincent)
        [Line 1] - Your Highlight on page 9 | location 69-70 | Added on Sunday, 17 July 2022 18:00:00
        [Line 2]
        [Line 3] Clipping content.
        [Line 4] ==========

        Returns:
            list[Clipping]: List of Clipping namedtuples.
        """

        clippings = []
        with open(self.path, "r", encoding="utf8") as file:
            line_number = 0
            while line := file.readline():
                if line_number == 0:
                    clipping = {**parse_book_line(line)}
                elif line_number == 1:
                    clipping = {**clipping, **parse_metadata_line(line)}
                elif line_number == 2:
                    pass
                elif line_number == 3:
                    clipping = {**clipping, **parse_content_line(line)}
                elif line_number == 4:
                    line_number = -1
                    try:
                        output = Clipping(**clipping, error=None)
                    except Exception as exc:
                        output = Clipping(**clipping, error=exc)
                    clippings.append(output)
                line_number += 1
        return clippings


def parse_book_line(line: str) -> dict:
    """
    Parses book line of Clipping with REGEX to extinguish Book title and author.

    Args:
        line (str): File line.

    Returns:
        dict: Dictionary containing Book namedtuple in "book" key or empty one.
    """
    line = line.replace("\xa0", " ").replace("\ufeff", "")
    if match := re.match(BOOK_WITH_PARENTHESES_REGEX, line):
        book_title, author = match.groups()
    elif match := re.match(BOOK_WITH_DASH_REGEX, line):
        book_title, author = match.groups()
    else:
        return {}
    return {"book": Book(title=book_title.strip(), author=author.strip())}


def parse_metadata_line(line: str) -> dict:
    """
    Parses metadata line of Clipping with REGEX to extinguish Clipping metadata - Clipping type, page number,
    location and creation datetime.

    Args:
        line (str): File line.

    Returns:
        dict: Dictionary containing Clipping metadata or empty one.
    """
    data = {}
    if match := re.match(METADATA_WITH_PAGE_REGEX, line):
        groups = match.groups()
        data["clipping_type"] = groups[0]
        data["page_number"] = groups[1]
        data["location"] = groups[3]
        data["created_at"] = datetime.strptime(groups[5], "%d %B %Y %H:%M:%S")
    elif match := re.match(METADATA_WITHOUT_PAGE_REGEX, line):
        groups = match.groups()
        data["clipping_type"] = groups[0]
        data["page_number"] = None
        data["location"] = groups[1]
        data["created_at"] = datetime.strptime(groups[3], "%d %B %Y %H:%M:%S")
    return data


def parse_content_line(line: str) -> dict:
    """
    Parses content line of Clipping to get rid of unnecessary signs.

    Args:
        line (str): File line.

    Returns:
        dict: Dictionary containing cleared "content" key data.
    """
    return {"content": line.replace("\xa0", " ").strip()}
