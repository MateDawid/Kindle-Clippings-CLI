from io import StringIO
from typing import Any
from unittest.mock import MagicMock, patch

import pytest
from clippings_cli.clippings_service.service import ClippingsService


@pytest.fixture
def clippings_service() -> ClippingsService:
    """
    Fixture for ClippingsService test instance.

    Returns:
        ClippingsService: ClippingsService test instance.
    """
    input_path = "path/to/input.txt"
    output_path = "path/to/output.json"
    return ClippingsService(input_path=input_path, output_path=output_path)


class TestClippingsService:
    """
    Tests for clippings_service.service.py.
    """

    @patch("builtins.open", new_callable=MagicMock)
    def test_parse_clippings(
        self,
        mock_open: MagicMock,
        clippings_service: ClippingsService,
        clippings_input: str,
        clippings_list: list[dict[str, Any]],
    ):
        """
        GIVEN: ClippingsService instance and Clippings input file.
        WHEN: Calling _parse_clippings() of ClippingsService with access to input file.
        THEN: Expected Clippings list returned.
        """
        mock_open.return_value = StringIO(clippings_input)

        clippings = clippings_service._parse_clippings()

        assert len(clippings) == 3
        assert clippings == clippings_list

    @patch("clippings_cli.clippings_service.service.generate_json")
    def test_generate_output_json(
        self, mock_generate_json: MagicMock, clippings_service: ClippingsService, clippings_list: list[dict[str, Any]]
    ):
        """
        GIVEN: ClippingsService instance and Clippings input file.
        WHEN: Calling generate_output() of ClippingsService with 'json' param.
        THEN: generate_json() method called once with clippings_list.
        """
        clippings_service._parse_clippings = MagicMock(return_value=clippings_list)
        mock_generate_json.return_value = {}

        result = clippings_service.generate_output("json")

        mock_generate_json.assert_called_once_with(clippings=clippings_list, output_path=clippings_service.output_path)
        assert result == {}

    @patch("clippings_cli.clippings_service.service.generate_excel")
    def test_generate_output_excel(
        self, mock_generate_excel: MagicMock, clippings_service: ClippingsService, clippings_list: list[dict[str, Any]]
    ):
        """
        GIVEN: ClippingsService instance and Clippings input file.
        WHEN: Calling generate_output() of ClippingsService with 'excel' param.
        THEN: generate_excel() method called once with clippings_list.
        """
        clippings_service._parse_clippings = MagicMock(return_value=clippings_list)
        mock_generate_excel.return_value = {}

        result = clippings_service.generate_output("excel")

        mock_generate_excel.assert_called_once_with(clippings=clippings_list, output_path=clippings_service.output_path)
        assert result == {}

    def test_generate_output_unsupported(self, clippings_service: ClippingsService):
        """
        GIVEN: ClippingsService instance and Clippings input file.
        WHEN: Calling generate_output() of ClippingsService with 'unsupported' param.
        THEN: Result dict with "error" key returned.
        """
        clippings_service._parse_clippings = MagicMock(return_value=[])

        result = clippings_service.generate_output("unsupported")

        assert result == {"error": "Format not supported."}
