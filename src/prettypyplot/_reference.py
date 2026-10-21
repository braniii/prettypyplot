# -*- coding: utf-8 -*-
# BSD 3-Clause License
# Copyright (c) 2026, Daniel Nagel
# All rights reserved.
"""Build the API reference of the installed prettypyplot as markdown.

The reference is printed by `python -m prettypyplot api`, e.g. for coding
agents looking up the signatures and docstrings of the installed version.

"""

# ~~~ IMPORT ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from __future__ import annotations

import ast
import inspect
import re
import sys
import textwrap
from typing import TYPE_CHECKING

import prettypyplot as _pplt
from prettypyplot import colors as pclr

if TYPE_CHECKING:
    from collections.abc import Callable, Iterable, Sequence

# ~~~ CONSTANTS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
COLORMAPS = 'colormaps'
DOCS_URL = 'https://braniii.github.io/prettypyplot'
MAX_LINE_LENGTH = 79
SECTIONS = {
    'prettypyplot.style': 'Style',
    'prettypyplot.pyplot': 'Plotting',
    'prettypyplot.subplots': 'Subplots',
    'prettypyplot.texts': 'Text',
    'prettypyplot.colors': 'Colors',
}
HEADER = """\
# prettypyplot {version} API reference

All functions are available at the top level after
`import prettypyplot as pplt`. Signatures are shown as written in the source.
Parameters documented as `args, kwargs` are passed on to the matplotlib
function of the same name.
"""


# ~~~ FUNCTIONS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def reference(names: Sequence[str] = ()) -> str:
    """Return the API reference as markdown.

    Parameters
    ----------
    names : sequence of str, optional
        Public functions to include and `'colormaps'` for the registered
        colormaps. If empty, the complete reference is returned.

    Returns
    -------
    text : str
        The reference in markdown.

    """
    available = (*_pplt.__all__, COLORMAPS)
    unknown = [name for name in names if name not in available]
    if unknown:
        raise ValueError(
            'Unknown name(s): {0}. Choose from: {1}.'.format(
                ', '.join(unknown),
                ', '.join(sorted(available)),
            ),
        )

    if names:
        return '\n'.join(
            _colormaps() if name == COLORMAPS else _function(name)
            for name in dict.fromkeys(names)
        )

    parts = [HEADER.format(version=_pplt.__version__)]
    for section, section_names in _functions_by_section(_pplt.__all__):
        parts.append('## {0}\n'.format(section))
        parts.extend(_function(name) for name in section_names)
    parts.append(_colormaps())
    return '\n'.join(parts)


def _function(name: str) -> str:
    """Return the reference of a single public function."""
    func = getattr(_pplt, name)
    return '### `pplt.{0}`\n\n```python\n{1}\n```\n\n```text\n{2}\n```\n'.format(
        name,
        _signature(name, func),
        _clean_docstring(_docstring(func)),
    )


def _functions_by_section(
    names: Iterable[str],
) -> Iterable[tuple[str, list[str]]]:
    """Group functions by module and sort them in source order."""
    grouped = {}
    for name in names:
        grouped.setdefault(getattr(_pplt, name).__module__, []).append(name)

    order = list(SECTIONS)
    for module in sorted(
        grouped,
        key=lambda mod: order.index(mod) if mod in order else len(order),
    ):
        yield (
            SECTIONS.get(module, module),
            sorted(
                grouped[module],
                key=lambda name: inspect.getsourcelines(getattr(_pplt, name))[1],
            ),
        )


def _function_node(func: Callable) -> ast.FunctionDef:
    """Return the ast node of the definition of func."""
    return ast.parse(textwrap.dedent(inspect.getsource(func))).body[0]


def _format_param(arg: ast.arg, default: ast.expr | None) -> str:
    """Format a single parameter with annotation and default value."""
    param = arg.arg
    if arg.annotation is not None:
        param += ': {0}'.format(ast.unparse(arg.annotation))
        if default is not None:
            param += ' = {0}'.format(ast.unparse(default))
    elif default is not None:
        param += '={0}'.format(ast.unparse(default))
    return param


def _signature(name: str, func: Callable) -> str:
    """Return the signature of func as written in the source code."""
    node = _function_node(func)
    args = node.args

    positional = args.posonlyargs + args.args
    defaults = [None] * (len(positional) - len(args.defaults)) + args.defaults
    params = [_format_param(arg, dflt) for arg, dflt in zip(positional, defaults)]
    if args.vararg is not None:
        params.append('*{0}'.format(_format_param(args.vararg, None)))
    elif args.kwonlyargs:
        params.append('*')
    params.extend(
        _format_param(arg, dflt) for arg, dflt in zip(args.kwonlyargs, args.kw_defaults)
    )
    if args.kwarg is not None:
        params.append('**{0}'.format(_format_param(args.kwarg, None)))

    returns = ''
    if node.returns is not None:
        returns = ' -> {0}'.format(ast.unparse(node.returns))

    one_line = 'pplt.{0}({1}){2}'.format(name, ', '.join(params), returns)
    if len(one_line) <= MAX_LINE_LENGTH:
        return one_line
    lines = ''.join('    {0},\n'.format(param) for param in params)
    return 'pplt.{0}(\n{1}){2}'.format(name, lines, returns)


def _docstring(func: Callable) -> str:
    """Return the docstring of func independent of the Python version.

    The docstring is taken from the source, because before Python 3.13 the
    runtime docstring of functions decorated with `copy_doc_params` mixes
    indentation levels.

    """
    node = _function_node(func)
    doc = ast.get_docstring(node)
    for decorator in node.decorator_list:
        is_copy_doc = isinstance(decorator, ast.Call) and (
            ast.unparse(decorator.func).endswith('copy_doc_params')
        )
        if is_copy_doc:
            # same as decorit.copy_doc_params, append Parameters of the source
            module = sys.modules[func.__module__]
            source_doc = _docstring(getattr(module, decorator.args[0].id))
            doc = '{0}\n\n{1}'.format(
                doc.rstrip(),
                source_doc[source_doc.find('Parameters') :],
            )
    return doc


def _clean_docstring(doc: str) -> str:
    """Convert the mkdocs specific markup to plain text."""
    # cross references [title][identifier] and [identifier][]
    doc = re.sub(r'\[`?([^\]`]+)`?\]\[[^\]]*\]', r'`\1`', doc)
    # cross references with missing brackets, e.g. [matplotlib.axes.Axes]
    doc = re.sub(r'\[((?:matplotlib|prettypyplot)[\w.]*)\](?![(\[])', r'`\1`', doc)
    # relative links into the documentation
    doc = re.sub(r'\]\((?:\.\./)+([^)]*)\)', r']({0}/\1)'.format(DOCS_URL), doc)
    # admonitions
    return re.sub(
        r'^!!! (\w+)$',
        lambda match: '{0}:'.format(match.group(1).capitalize()),
        doc,
        flags=re.MULTILINE,
    )


def _colormaps() -> str:
    """Return the table of all colormaps defined in prettypyplot."""
    factories = [
        obj
        for name, obj in vars(pclr).items()
        if name.startswith('_')
        and callable(obj)
        and getattr(obj, '__module__', '').startswith('prettypyplot._cmaps')
    ]
    cmaps = sorted((factory() for factory in factories), key=lambda cm: cm.name)
    return (
        '## Registered colormaps\n\n'
        'Registered by `pplt.use_style()` (or `pplt.load_cmaps()`), each also\n'
        'reversed as `<name>_r`. Discrete colormaps can be used as color cycle\n'
        "with `pplt.use_style(colors='<name>')`, continuous ones are sampled at\n"
        '`ncs` points. All matplotlib colormaps can be used as well.\n\n'
        '| Name | Kind | Colors |\n| --- | --- | --- |\n'
        + ''.join(
            '| `{0}` | {1} | {2} |\n'.format(
                cmap.name,
                'discrete' if cmap.N < 256 else 'continuous',
                cmap.N if cmap.N < 256 else '-',
            )
            for cmap in cmaps
        )
    )
