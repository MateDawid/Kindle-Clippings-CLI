import json
import os
from pathlib import Path
from typing import Any
from unittest import mock

import pytest
from clippings_cli.clippings_service.format_handlers.json_handlers import generate_json


@pytest.fixture
def output_json_path(tmp_path: Path) -> str:
    """
    Returns path to output file in temporary location.

    Args:
        tmp_path (Path): Temporary pytest files location.

    Returns:
         str: Path to output file in temporary pytest files location.
    """
    return os.path.normpath(os.path.join(tmp_path, "subdir", "output.json"))


class TestJsonHandlers:
    """Tests for clippings_service.format_handlers.json_handlers.py."""

    def test_generate_json_success(self, output_json_path: str, clippings_list: list[dict[str, Any]]):
        """
        GIVEN: Clippings list.
        WHEN: Calling generate_json() function with clippings and output path.
        THEN: JSON file generated and containing clippings data.
        """
        result = generate_json(clippings_list, output_json_path)

        assert result == {}
        assert os.path.exists(output_json_path)

        with open(output_json_path, "r", encoding="utf-8") as json_file:
            data = json.load(json_file)
            assert data == clippings_list

    def test_generate_json_permission_error(self, output_json_path, clippings_list: list[dict[str, Any]]):
        """
        GIVEN: List containing two clippings.
        WHEN: Calling generate_json() function with clippings and inaccessible output path.
        THEN: PermissionError raised and handled.
        """
        with mock.patch("builtins.open", side_effect=PermissionError("Permission denied")):
            result = generate_json(clippings_list, output_json_path)

        assert "error" in result
        assert isinstance(result["error"], PermissionError)
        assert str(result["error"]) == "Permission denied"
