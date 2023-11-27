import pathlib
from collections import defaultdict

import setuptools


def get_extra_requirements(path, add_all=True):
    """Parse extra-requirements file."""

    with open(path) as depfile:
        extra_deps = defaultdict(set)
        for line in depfile:
            if not line.startswith('#'):
                if ':' not in line:
                    raise ValueError(
                        f'Dependency in {path} not correct formatted: {line}',
                    )
                dep, tags = line.split(':')
                tags = {tag.strip() for tag in tags.split(',')}
                for tag in tags:
                    extra_deps[tag].add(dep)

        # add tag `all` at the end
        if add_all:
            extra_deps['all'] = {
                tag for tags in extra_deps.values() for tag in tags
            }

    return extra_deps


# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / 'README.md').read_text()

# This call to setup() does all the work
setuptools.setup(
    name='prettypyplot',
    version='0.10.1',
    description='Wrapper for matplotlib to generate pretty plots.',
    long_description=README,
    long_description_content_type='text/markdown',
    keywords='matplotlib pyplot',
    author='braniii',
    url='https://gitlab.com/braniii/prettypyplot',
    license='BSD 3-Clause License',
    license_files=('LICENSE', ),
    classifiers=[
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    package_dir={'': 'src'},
    packages=setuptools.find_packages(where='src'),
    python_requires='>=3.6',
    include_package_data=True,
    install_requires=[
        'matplotlib',
        'numpy',
        'decorit>=0.2.0',
    ],
    extras_require=get_extra_requirements('extra-requirements.txt')
)
