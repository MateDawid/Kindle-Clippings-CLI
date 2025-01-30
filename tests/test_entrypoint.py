from click.testing import CliRunner
from entrypoint import cli


def test_cli():
    """
    GIVEN: clippings_cli installed.
    WHEN: Calling "clippings_cli" command.
    THEN:
    """
    runner = CliRunner()

    result = runner.invoke(cli)

    assert "CLI for reading data from Kindle MyClippings.txt file." in result.stdout
    assert "--help  Show this message and exit." in result.stdout
    assert "convert  Convert Clippings file to one of supported formats."
    assert result.return_value is None
    assert result.exit_code == 0
