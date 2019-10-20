import pathlib
import setuptools

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setuptools.setup(
    name="prettypyplot",
    version="0.1",
    description="Wrapper for matplotlib to generate pretty plots.",
    long_description=README,
    long_description_content_type="text/markdown",
    keywords="matplotlib pyplot",
    author="braniii",
    author_email="braniii@mail.com",
    url="https://gitlab.com/braniii/prettyplot",
    license="BSD 3-Clause License",
    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=setuptools.find_packages(exclude=('tests', 'docs')),
    include_package_data=True,
    install_requires=["matplotlib", "numpy"],
)