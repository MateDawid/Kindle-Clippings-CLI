import click
from clippings_cli.commands.convert import convert


@click.group()
def cli():
    """CLI for reading data from Kindle MyClippings.txt file."""
    pass


cli.add_command(convert)
