import os

import click


def get_full_path(path: str | None) -> str | None:
    """
    Function to evaluate full path to Clippings file based on input path.

    Args:
        path (str | None): Path to Clippings file or None.

    Returns:
        str | None: Full path to Clippings file or None in case of errors.
    """
    if not path:
        path = os.path.normpath(os.path.join(os.getcwd(), "My Clippings.txt"))
    elif os.path.isabs(os.path.normpath(path)):
        pass
    else:
        path = os.path.normpath(os.path.join(os.getcwd(), path))
    if not os.path.exists(path):
        click.echo(click.style(f"Path [{path}] does not exist.", fg="red", underline=True), err=True)
        return None
    elif not os.path.isfile(path):
        click.echo(click.style(f"Path [{path}] is not a file.", fg="red", underline=True), err=True)
        return None
    elif not path.endswith(".txt"):
        click.echo(click.style(f"Path [{path}] is not a .txt file.", fg="red", underline=True), err=True)
        return None
    return path


@click.command()
@click.option("-p", "--path", default=None, help="Path to Clippings file (full or relative).")
@click.option(
    "-f",
    "--format",
    required=True,
    type=click.Choice(["json", "excel"], case_sensitive=False),
    help="Output format. [json|excel]",
)
def convert(path: str | None, format: str):
    """
    Convert Clippings file to one of supported formats. [json|excel]

    Args:

        path (str | None): Full or relative path to Clippings file. Searches for "My Clipping.txt" file in current
        directory by default.

        format (str): Demanded format of output. [json|excel]
    """

    full_path = get_full_path(path)
    if full_path is None:
        exit()
    click.echo(click.style(f"Clippings file [{full_path}] processing started.", fg="yellow", underline=True), err=False)
