# -*- coding: utf-8 -*-
"""Tests for the agent skill in skills/prettypyplot.

BSD 3-Clause License
Copyright (c) 2026, Daniel Nagel
All rights reserved.

"""

import json
import re
import runpy
from pathlib import Path

import matplotlib as mpl
import pytest
from matplotlib import pyplot as plt

import prettypyplot
from prettypyplot import _reference

ROOT = Path(__file__).parents[1]
SKILL_DIR = ROOT / 'skills' / 'prettypyplot'
SKILL_MD = SKILL_DIR / 'SKILL.md'
GUIDES = (SKILL_MD, SKILL_DIR / 'references' / 'style.md')
EXAMPLES = sorted((SKILL_DIR / 'examples').glob('*.py'))


def _frontmatter(path):
    """Parse the flat YAML frontmatter of a markdown file."""
    match = re.match(r'---\n(.*?)\n---\n', path.read_text(), re.DOTALL)
    assert match, 'missing frontmatter in {0}'.format(path)
    return dict(line.split(': ', 1) for line in match.group(1).splitlines())


@pytest.fixture
def isolated_style(tmp_path, monkeypatch):
    """Run in a temporary directory and restore the global style afterwards."""
    monkeypatch.chdir(tmp_path)
    style, mode = prettypyplot.STYLE, prettypyplot.MODE
    style_dict = dict(prettypyplot.STYLE_DICT)
    with mpl.rc_context():
        yield tmp_path
        plt.close('all')
    prettypyplot.STYLE, prettypyplot.MODE = style, mode
    prettypyplot.STYLE_DICT.clear()
    prettypyplot.STYLE_DICT.update(style_dict)


@pytest.mark.parametrize('path', GUIDES, ids=lambda path: path.name)
def test_referenced_api_exists(path):
    """Functions and `api` commands in the guides exist in prettypyplot."""
    text = path.read_text()
    functions = set(re.findall(r'\bpplt\.(\w+)', text))
    assert functions
    unknown = functions - set(prettypyplot.__all__)
    assert not unknown, unknown

    for names in re.findall(r'prettypyplot api ([a-z_][a-z_ ]*)', text):
        _reference.reference(names.split())


@pytest.mark.parametrize('path', GUIDES, ids=lambda path: path.name)
def test_guide_code_blocks(path, isolated_style):
    """All python code blocks of a guide run in one shared namespace."""
    blocks = re.findall(r'```python\n(.*?)```', path.read_text(), re.DOTALL)
    assert blocks

    namespace = {}
    for block in blocks:
        exec(compile(block, str(path), 'exec'), namespace)  # noqa: S102


@pytest.mark.parametrize('path', EXAMPLES, ids=lambda path: path.name)
def test_examples(path, isolated_style):
    """All examples run and save a figure."""
    runpy.run_path(str(path), run_name='__main__')
    assert any(isolated_style.iterdir())


@pytest.mark.parametrize('path', GUIDES, ids=lambda path: path.name)
def test_relative_links(path):
    """Relative links in the guides point to existing files and headings."""
    links = re.findall(r'\]\(([^)#:]*)(?:#([^)]*))?\)', path.read_text())
    assert links
    for target, anchor in links:
        target = path.parent / target if target else path
        assert target.exists(), target
        if anchor:
            headings = re.findall(r'^#+ (.+)$', target.read_text(), re.MULTILINE)
            slugs = {
                re.sub(r'[^\w\- ]', '', heading).lower().replace(' ', '-')
                for heading in headings
            }
            assert anchor in slugs, '{0}#{1}'.format(target.name, anchor)


def test_skill_frontmatter():
    """The frontmatter follows the Agent Skills specification."""
    meta = _frontmatter(SKILL_MD)
    assert meta['name'] == SKILL_DIR.name
    assert re.fullmatch(r'[a-z0-9]+(-[a-z0-9]+)*', meta['name'])
    assert len(meta['name']) <= 64
    assert 0 < len(meta['description']) <= 1024
    assert len(SKILL_MD.read_text().splitlines()) < 500


def test_plugin_manifests():
    """Plugin and marketplace manifests are consistent with the package."""
    plugin_dir = ROOT / '.claude-plugin'
    plugin = json.loads((plugin_dir / 'plugin.json').read_text())
    marketplace = json.loads((plugin_dir / 'marketplace.json').read_text())

    assert [entry['name'] for entry in marketplace['plugins']] == [plugin['name']]

    # the skill is updated for users only if the version changes
    version = re.search(
        r'^version = "(.+)"$',
        (ROOT / 'pyproject.toml').read_text(),
        re.MULTILINE,
    ).group(1)
    assert plugin['version'] == version
