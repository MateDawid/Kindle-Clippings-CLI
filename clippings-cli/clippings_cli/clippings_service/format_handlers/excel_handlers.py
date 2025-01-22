"""
File containing functions for handling Excel Clippings file.
"""

# TODO: Excel styling

import os
from collections import OrderedDict
from typing import Callable

from openpyxl.workbook import Workbook

FIELDS: OrderedDict[str, Callable] = OrderedDict(
    [
        ("Book title", lambda clipping: clipping["book"]["title"]),
        ("Book author", lambda clipping: clipping["book"]["author"]),
        ("Content", lambda clipping: clipping["content"]),
        ("Page number", lambda clipping: clipping["page_number"]),
        ("Location", lambda clipping: clipping["location"]),
        ("Created at", lambda clipping: clipping["created_at"]),
        ("Clipping type", lambda clipping: clipping["clipping_type"]),
        ("Errors", lambda clipping: str(clipping["errors"])),
    ]
)


def generate_excel(clippings: list[dict], output_path: str) -> dict:
    """
    In provided output_path creates Excel file containing data collected from Clippings input file.

    Args:
        clippings (list[dict]): List of collected Clippings.
        output_path (str): Full path to output file.

    Returns:
        dict: Dictionary containing data about potential errors.
    """

    # Create a new workbook and select the active worksheet
    wb = Workbook()
    ws = wb.active
    ws.append(list(FIELDS.keys()))

    for clipping in clippings:
        ws.append([FIELDS[key](clipping) for key in FIELDS])

    try:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        wb.save(output_path)
    except PermissionError as e:
        return {"error": e}
    return {}
