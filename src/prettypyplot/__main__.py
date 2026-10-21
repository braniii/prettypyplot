# -*- coding: utf-8 -*-
# BSD 3-Clause License
# Copyright (c) 2026, Daniel Nagel
# All rights reserved.
"""Command line interface of prettypyplot, run `python -m prettypyplot`."""

# ~~~ IMPORT ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import click

from prettypyplot import _reference


# ~~~ COMMANDS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@click.group()
@click.version_option(package_name='prettypyplot')
def main():
    """Command line interface of prettypyplot."""


@main.command()
@click.argument('names', nargs=-1)
def api(names):
    """Print the API reference of the installed prettypyplot.

    Without NAMES, all public functions and the registered colormaps are
    printed. Otherwise only the given functions, e.g. `legend colorbar`, and
    `colormaps` for the table of colormaps.
    """
    try:
        text = _reference.reference(names)
    except ValueError as err:
        raise click.BadParameter(str(err), param_hint='NAMES') from err
    click.echo(text)


if __name__ == '__main__':
    main(prog_name='python -m prettypyplot')
