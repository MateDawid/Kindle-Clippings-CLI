"""
File containing data parsers for ClippingsService class.
"""


def validate_fields(clipping: dict) -> dict:
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
