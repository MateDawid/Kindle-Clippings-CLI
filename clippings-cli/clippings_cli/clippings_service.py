"""
File containing ClippingsService class that manages Clippings import from input file and content
conversion to one of supported formats.

Constants:
    BOOK_WITH_PARENTHESES_REGEX (str) - Regex to handle book title Clipping line, like "Book title (Book author)".
    BOOK_WITH_DASH_REGEX (str) - Regex to handle book title Clipping line, like "Book title - Book author".
    METADATA_WITH_PAGE_REGEX (str) - Regex to handle Clipping metadata line with page as first mentioned param, like
    "- Your Highlight on page 3 | location 41-41 | Added on Monday, 6 February 2023 06:32:11"
    METADATA_WITHOUT_PAGE_REGEX (str) - Regex to handle Clipping metadata line without page as first mentioned
    param, like "- Your Bookmark at location 579 | Added on Tuesday, 27 September 2022 15:45:30".
"""
import json
import os
import re
from datetime import datetime

BOOK_WITH_PARENTHESES_REGEX: str = r"^(.*) \((.*)\)$"
BOOK_WITH_DASH_REGEX: str = r"^(.*) - (.*)$"
METADATA_WITH_PAGE_REGEX: str = (
    r"^- Your (\w+) on page (\d+|\d+-\d+) \| (location (\d+|\d+-\d+) \| )?Added on (\w+), (.*)$"
)
METADATA_WITHOUT_PAGE_REGEX: str = r"^- Your (\w+) at location (\d+|\d+-\d+) \| Added on (\w+), (.*)$"


class ClippingsService:
    """
    Class for retrieving Clippings from input Clippings file.

    Args:
        input_path (str): Full path to input Clippings file.
        output_path (str): Full path to output file.

    Attributes:
        clippings (list[dict]): List of collected Clippings.
    """

    def __init__(self, input_path: str, output_path: str):
        self.input_path: str = input_path
        self.output_path: str = output_path
        self.clippings: list[dict] = self._parse_clippings()

    def _parse_clippings(self) -> list[dict]:
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
        with open(self.input_path, "r", encoding="utf8") as file:
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
                    clipping["errors"] = validate_clipping(clipping)
                    clippings.append(clipping)
                    clipping = {}
                line_number += 1
        return clippings

    def return_as_json(self) -> dict:
        """
        In provided output_path creates JSON file containing data collected from Clippings input file.

        Returns:
            dict: Dictionary containing data about potential errors.
        """
        try:
            os.makedirs(os.path.dirname(self.output_path), exist_ok=True)
            with open(self.output_path, "w", encoding="utf-8") as json_file:
                json.dump(self.clippings, json_file, ensure_ascii=False, indent=4)
        except PermissionError as e:
            return {"error": e}
        return {}


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
    return {"book": {"title": book_title.strip(), "author": author.strip()}}


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
        data["created_at"] = datetime.strptime(groups[5], "%d %B %Y %H:%M:%S").strftime("%Y-%m-%d %H:%M:%S")
    elif match := re.match(METADATA_WITHOUT_PAGE_REGEX, line):
        groups = match.groups()
        data["clipping_type"] = groups[0]
        data["page_number"] = None
        data["location"] = groups[1]
        data["created_at"] = datetime.strptime(groups[3], "%d %B %Y %H:%M:%S").strftime("%Y-%m-%d %H:%M:%S")
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


def validate_clipping(clipping: dict) -> dict:
    """
    Validates Clipping content after parsing.

    Args:
        clipping (dict): Parsed Clipping data.

    Returns:
        dict: Dictionary containing errors found in Clipping dictionary.
    """
    errors = {}
    for field in ("book", "clipping_type", "page_number", "created_at", "location", "content"):
        if field not in clipping:
            errors[field] = f"Field {field} missed in Clipping."
    return errors
