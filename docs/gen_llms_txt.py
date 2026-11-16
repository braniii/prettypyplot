"""Generate llms.txt and llms-full.txt for coding agents.

Both files are built from the agent skill in skills/prettypyplot and the API
reference printed by `python -m prettypyplot api`, see https://llmstxt.org for
the format.

"""

import re
from pathlib import Path

import mkdocs_gen_files

from prettypyplot._reference import reference

SKILL_DIR = Path('skills/prettypyplot')
SITE_URL = 'https://braniii.github.io/prettypyplot'
REPO_URL = 'https://github.com/braniii/prettypyplot/blob/main'

LLMS_TXT = f"""\
# prettypyplot

> prettypyplot (`import prettypyplot as pplt`) is a small wrapper around
> matplotlib. `pplt.use_style()` sets publication-ready defaults, a few
> wrappers add legends outside the axes, colorbars and subplot helpers, and
> `pplt.savefig` treats `figsize` as the size of the axes. Everything else is
> plain matplotlib.

Read the usage guide before writing code: prettypyplot changes several
matplotlib defaults, and whether text is rendered with LaTeX depends on the
machine. The API reference of the installed version is printed by
`python -m prettypyplot api [NAME ...]`.

## Docs

- [Usage guide for coding agents]({SITE_URL}/llms-full.txt): rules, pitfalls,
  style guide, full API reference and examples in a single file
- [Overview]({SITE_URL}/): installation and comparison with matplotlib
- [Gallery]({SITE_URL}/gallery/): examples for legends, colorbars and colormaps
- [Code reference]({SITE_URL}/reference/): API documentation

## Optional

- [Agent skill]({REPO_URL}/skills/prettypyplot/SKILL.md): install in Claude
  Code with `/plugin marketplace add braniii/prettypyplot`
- [Changelog]({SITE_URL}/changelog/)
"""


def read_markdown(path):
    """Return content of markdown file without YAML frontmatter."""
    return re.sub(r'\A---\n.*?\n---\n+', '', path.read_text(), flags=re.DOTALL)


def build_full():
    """Concatenate the skill, the style guide, API reference and examples."""
    parts = [
        read_markdown(SKILL_DIR / 'SKILL.md'),
        read_markdown(SKILL_DIR / 'references' / 'style.md'),
        reference(),
    ]
    for example in sorted((SKILL_DIR / 'examples').glob('*.py')):
        parts.append(
            '# Example `{0}`\n\n```python\n{1}```\n'.format(
                example.name,
                example.read_text(),
            ),
        )
    return '\n\n'.join(part.strip() + '\n' for part in parts)


with mkdocs_gen_files.open('llms.txt', 'w') as fd:
    fd.write(LLMS_TXT)

with mkdocs_gen_files.open('llms-full.txt', 'w') as fd:
    fd.write(build_full())
