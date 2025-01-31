import os
from unittest.mock import MagicMock, patch

import pytest
from click.testing import CliRunner
from commands.convert import convert, get_full_input_path, get_full_output_path


class TestGetFullInputPath:
    """
    get_full_input_path function tests.
    """

    @pytest.mark.parametrize(
        "path, expected_output",
        (
            pytest.param(None, os.path.normpath(os.path.join(os.getcwd(), "My Clippings.txt")), id="no-path-provided"),
            pytest.param(
                os.path.normpath(os.path.join(os.getcwd(), "My Clippings.txt")),
                os.path.normpath(os.path.join(os.getcwd(), "My Clippings.txt")),
                id="absolute-path",
            ),
            pytest.param(
                "subdir/My Clippings.txt",
                os.path.normpath(os.path.join(os.getcwd(), "subdir/My Clippings.txt")),
                id="relative-path",
            ),
        ),
    )
    @patch("os.path.exists", return_value=True)
    @patch("os.path.isfile", return_value=True)
    def test_get_full_input_path_successful(
        self, mock_isfile: MagicMock, mock_exists: MagicMock, path: str | None, expected_output: str | None
    ):
        """
        GIVEN: Valid input file path - string or None.
        WHEN: Calling get_full_input_path function with path.
        THEN: Function output the same as expected.
        """
        result = get_full_input_path(path)

        assert result == expected_output

    @patch("os.path.exists", return_value=False)
    def test_get_full_input_path_not_exists(self, mock_exists: MagicMock):
        """
        GIVEN: Not existing input file path.
        WHEN: Calling get_full_input_path function with path.
        THEN: Function returned None.
        """
        result = get_full_input_path("Clippings.txt")

        assert result is None

    @patch("os.path.exists", return_value=True)
    @patch("os.path.isfile", return_value=False)
    def test_get_full_input_path_is_not_a_file(self, mock_isfile: MagicMock, mock_exists: MagicMock):
        """
        GIVEN: Directory path passed as input file path.
        WHEN: Calling get_full_input_path function with path.
        THEN: Function returned None.
        """
        result = get_full_input_path("clippings/clippings")

        assert result is None

    @patch("os.path.exists", return_value=True)
    @patch("os.path.isfile", return_value=True)
    def test_get_full_input_path_is_not_txt_file(self, mock_isfile: MagicMock, mock_exists: MagicMock):
        """
        GIVEN: Not a .txt file path passed as input file path.
        WHEN: Calling get_full_input_path function with path.
        THEN: Function returned None.
        """
        result = get_full_input_path("clippings/clippings.xml")

        assert result is None


class TestGetFullOutputPath:
    """
    get_full_output_path function tests.
    """

    @pytest.mark.parametrize(
        "path, format, expected_output",
        (
            pytest.param(None, "json", os.path.normpath(os.path.join(os.getcwd(), "Output.json")), id="default-json"),
            pytest.param(None, "excel", os.path.normpath(os.path.join(os.getcwd(), "Output.xlsx")), id="default-excel"),
            pytest.param(
                os.path.normpath(os.path.join(os.getcwd(), "subdir", "Absolute.json")),
                "json",
                os.path.normpath(os.path.join(os.getcwd(), "subdir", "Absolute.json")),
                id="absolute-json",
            ),
            pytest.param(
                os.path.normpath(os.path.join(os.getcwd(), "subdir", "Absolute.xlsx")),
                "excel",
                os.path.normpath(os.path.join(os.getcwd(), "subdir", "Absolute.xlsx")),
                id="absolute-excel",
            ),
            pytest.param(
                os.path.normpath(os.path.join("subdir", "Absolute.json")),
                "json",
                os.path.normpath(os.path.join(os.getcwd(), "subdir", "Absolute.json")),
                id="relative-json",
            ),
            pytest.param(
                os.path.normpath(os.path.join("subdir", "Absolute.xlsx")),
                "excel",
                os.path.normpath(os.path.join(os.getcwd(), "subdir", "Absolute.xlsx")),
                id="relative-excel",
            ),
        ),
    )
    def test_get_full_output_path_successful(self, path: str | None, format: str, expected_output: str | None):
        """
        GIVEN: Valid output file path - string or None.
        WHEN: Calling get_full_output_path function with path and format.
        THEN: Function output the same as expected.
        """
        result = get_full_output_path(path, format)

        assert result == expected_output

    @pytest.mark.parametrize("format", (None, "invalid"))
    def test_get_full_output_path_invalid_format(self, format: str | None):
        """
        GIVEN: Invalid format for output file.
        WHEN: Calling get_full_output_path function with path.
        THEN: Function returned None.
        """
        result = get_full_output_path("Output.json", format)

        assert result is None


@patch("commands.convert.ClippingsService.generate_output")
class TestConvert:
    """
    "clippings_cli convert" command tests.
    """

    @patch("commands.convert.get_full_output_path")
    @patch("commands.convert.get_full_input_path")
    @pytest.mark.parametrize(
        "args",
        [
            pytest.param(["--format", "json"], id="--format-json"),
            pytest.param(["--format", "excel"], id="--format-excel"),
            pytest.param(["-f", "json"], id="-f-json"),
            pytest.param(["-f", "excel"], id="-f-excel"),
            pytest.param(["-f", "json", "--input_path", "C:\\my_fancy_clippings.txt"], id="--input_path"),
            pytest.param(["-f", "json", "-i", "C:\\my_fancy_clippings.txt"], id="-i"),
            pytest.param(["-f", "json", "--output_path", "C:\\my_fancy_clippings.json"], id="--output_path"),
            pytest.param(["-f", "json", "-o", "C:\\my_fancy_clippings.json"], id="-o"),
        ],
    )
    def test_convert_successful(
        self, mocked_input_path: MagicMock, mocked_output_path: MagicMock, mocked_generate_output: MagicMock, args: list
    ):
        """
        GIVEN: clippings_cli installed, input .txt file exists and output path accessible.
        WHEN: Calling "clippings_cli convert" command with --format or -f .
        THEN: Logs in stdout, command existed with 0 code.
        """
        input_path = "C:\\My Clippings.txt"
        match args[1]:
            case "json":
                output_path = "C:\\Clippings.json"
            case "excel":
                output_path = "C:\\Clippings.xlsx"
            case _:
                output_path = None
        if "-i" in args:
            input_path = args[args.index("-i") + 1]
        elif "--input_path" in args:
            input_path = args[args.index("--input_path") + 1]
        if "-o" in args:
            output_path = args[args.index("-o") + 1]
        elif "--output_path" in args:
            output_path = args[args.index("--output_path") + 1]

        mocked_generate_output.return_value = {}
        mocked_input_path.return_value = input_path
        mocked_output_path.return_value = output_path
        runner = CliRunner()

        result = runner.invoke(convert, args)

        assert "Output file generation started" in result.stdout
        assert f"* Format [{args[1]}]" in result.stdout
        assert f"* Input path [{mocked_input_path.return_value}]" in result.stdout
        assert f"* Output path [{mocked_output_path.return_value}]" in result.stdout
        assert "Output file generation finished successfully." in result.stdout
        assert result.return_value is None
        assert result.exit_code == 0

    @patch("commands.convert.get_full_output_path")
    @patch("commands.convert.get_full_input_path")
    def test_convert_failed(
        self,
        mocked_input_path: MagicMock,
        mocked_output_path: MagicMock,
        mocked_generate_output: MagicMock,
    ):
        """
        GIVEN: clippings_cli installed, input .txt file exists and output path accessible.
        WHEN: Calling "clippings_cli convert" command with --format or -f.
        THEN: Logs in stdout, command existed with 1 code.
        """
        mocked_generate_output.return_value = {"error": "Generation failed."}
        mocked_input_path.return_value = "C:\\My Clippings.txt"
        mocked_output_path.return_value = "C:\\Clippings.json"
        runner = CliRunner()

        result = runner.invoke(convert, ["--format", "json"])

        assert "Output file generation started" in result.stdout
        assert "* Format [json]" in result.stdout
        assert f"* Input path [{mocked_input_path.return_value}]" in result.stdout
        assert f"* Output path [{mocked_output_path.return_value}]" in result.stdout
        assert (
            f"Output file in [json] format generation finished "
            f"with error [{mocked_generate_output.return_value['error']}]." in result.stdout
        )
        assert result.return_value is None
        assert result.exit_code == 1

    @patch("commands.convert.get_full_output_path")
    @patch("commands.convert.get_full_input_path")
    @pytest.mark.parametrize(
        "input_path",
        ["not\\existing\\path.txt", "not\\txt\\file.jpg", "not\\a\\file"],
    )
    def test_convert_invalid_input_path(
        self,
        mocked_input_path: MagicMock,
        mocked_output_path: MagicMock,
        mocked_generate_output: MagicMock,
        input_path: str,
    ):
        """
        GIVEN: clippings_cli installed, output path accessible.
        WHEN: Calling "clippings_cli convert" command with invalid --input_path param.
        THEN: Command existed with 1 code.
        """
        mocked_generate_output.return_value = {}
        mocked_input_path.return_value = None
        mocked_output_path.return_value = "C:\\Clippings.json"
        runner = CliRunner()

        result = runner.invoke(convert, ["--format", "json", "--input_path", input_path])

        assert result.return_value is None
        assert result.exit_code == 1
