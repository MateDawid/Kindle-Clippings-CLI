"""
File containing functions for handling Excel Clippings file.
"""

import os

from openpyxl.workbook import Workbook


def generate_excel(clippings: list[dict], output_path: str, *args, **kwargs) -> dict:
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

    # Write the header row
    headers = [
        "Clipping type",
        "Book title",
        "Book author",
        "Page number",
        "Location",
        "Created at",
        "Content",
        "Errors",
    ]
    ws.append(headers)

    # Write the data rows
    for row in clippings:
        ws.append(
            [
                row["clipping_type"],
                row["book"]["title"],
                row["book"]["author"],
                row["page_number"],
                row["location"],
                row["created_at"],
                row["content"],
                str(row["errors"]),
            ]
        )

    try:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        wb.save(output_path)
    except PermissionError as e:
        return {"error": e}
    return {}
