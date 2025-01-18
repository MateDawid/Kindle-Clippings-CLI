import re
from collections import namedtuple
from datetime import datetime

Book = namedtuple("Book", ["title", "author"])
Clipping = namedtuple("Clipping", ["book", "clipping_type", "page_number", "created_at", "location", "content"])


class ClippingsService:
    """
    Class for retrieving Clippings from input Clippings file.

    Args:
        path (str): Full path to Clippings file.

    Attributes:
        clippings (set[Book]): Set of Books.
        clippings (list[Clipping]): List of collected Clippings.
    """

    BOOK_WITH_PARENTHESES_REGEX = r"^(.*) \((.*)\)$"
    BOOK_WITH_DASH_REGEX = r"^(.*) - (.*)$"
    METADATA_WITH_PAGE_REGEX = (
        r"^- Your (\w+) on page (\d+|\d+-\d+) \| (location (\d+|\d+-\d+) \| )?Added on (\w+), (.*)$"
    )
    METADATA_WITHOUT_PAGE_REGEX = r"^- Your (\w+) at location (\d+|\d+-\d+) \| Added on (\w+), (.*)$"

    def __init__(self, path: str):
        self.path: str = path
        self.books: set[Book] = set()
        self.clippings: list[Clipping] = self._parse_clippings()

    def _parse_clippings(self) -> list[Clipping]:
        """
        Returns clippings from file and saves them in self.clippings dictionary.

        Example clipping:
        Django for APIs (William S. Vincent)
        - Your Highlight on page 9 | location 69-70 | Added on Sunday, 17 July 2022 18:00:00

        Clipping content.
        ==========
        """

        clippings = []
        with open(self.path, "r", encoding="utf8") as file:
            line_number = 0
            while line := file.readline():
                if line_number == 0:
                    clipping = {**self._parse_book_line(line)}
                elif line_number == 1:
                    clipping = {**clipping, **self._parse_metadata_line(line)}
                elif line_number == 2:
                    pass
                elif line_number == 3:
                    clipping = {**clipping, **self._parse_content_line(line)}
                elif line_number == 4:
                    line_number = -1
                    try:
                        output = Clipping(**clipping)
                    except Exception as exc:
                        print("ERROR: ", exc)
                        print(clipping)
                        break
                    clippings.append(output)
                line_number += 1
        return clippings

    def _parse_book_line(self, line: str):
        data = {}
        line = line.replace("\xa0", " ").replace("\ufeff", "")
        if match := re.match(self.BOOK_WITH_PARENTHESES_REGEX, line):
            book_title, author = match.groups()
        elif match := re.match(self.BOOK_WITH_DASH_REGEX, line):
            book_title, author = match.groups()
        else:
            return {}
        book = Book(title=book_title.strip(), author=author.strip())
        data["book"] = book
        self.books.add(book)
        return data

    def _parse_metadata_line(self, line: str):
        data = {}
        if match := re.match(self.METADATA_WITH_PAGE_REGEX, line):
            groups = match.groups()
            data["clipping_type"] = groups[0]
            data["page_number"] = groups[1]
            data["location"] = groups[3]
            data["created_at"] = datetime.strptime(groups[5], "%d %B %Y %H:%M:%S")
        elif match := re.match(self.METADATA_WITHOUT_PAGE_REGEX, line):
            groups = match.groups()
            data["clipping_type"] = groups[0]
            data["page_number"] = None
            data["location"] = groups[1]
            data["created_at"] = datetime.strptime(groups[3], "%d %B %Y %H:%M:%S")
        return data

    def _parse_content_line(self, line: str):
        return {"content": line.replace("\xa0", " ").strip()}
