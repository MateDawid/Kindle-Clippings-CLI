from unittest.mock import MagicMock, patch

import pytest
from click.testing import CliRunner
from clippings_cli.commands.convert import convert


class TestConvert:
    """
    "clippings_cli convert" command tests.
    """

    @patch("clippings_cli.commands.convert.get_full_output_path")
    @patch("clippings_cli.commands.convert.get_full_input_path", return_value="C:\\My Clippings.txt")
    @patch("clippings_cli.commands.convert.ClippingsService.generate_output", return_value={"test"})
    @pytest.mark.parametrize(
        "param, format, output_path",
        [
            pytest.param("--format", "json", "C:\\Clippings.json", id="format-json"),
            pytest.param("-f", "json", "C:\\Clippings.json", id="f-json"),
            pytest.param("--format", "excel", "C:\\Clippings.xlsx", id="format-excel"),
            pytest.param("-f", "excel", "C:\\Clippings.xlsx", id="f-excel"),
        ],
    )
    def test_convert_successful(
        self,
        mocked_generate_output: MagicMock,
        mocked_input_path: MagicMock,
        mocked_output_path: MagicMock,
        param: str,
        format: str,
        output_path: str,
    ):
        """
        GIVEN: clippings_cli installed, input .txt file exists and output path accessible.
        WHEN: Calling "clippings_cli convert" command with --format or -f .
        THEN: Logs in stdout, command existed with 0 code.
        """
        mocked_output_path.return_value = output_path
        runner = CliRunner()

        result = runner.invoke(convert, [param, format])

        assert "Output file generation started" in result.stdout
        assert f"* Format [{format}]" in result.stdout
        assert f"* Input path [{mocked_input_path.return_value}]" in result.stdout
        assert f"* Output path [{output_path}]" in result.stdout
        assert "Output file generation finished successfully." in result.stdout
        assert result.return_value is None
        assert result.exit_code == 0
