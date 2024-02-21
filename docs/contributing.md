# Welcome to the `prettypyplot` Contributing Guide

This guide will give you an overview of the contribution workflow from opening an issue and creating a PR. To get an overview of the project, read the [module overview][prettypyplot].

## Issues

### Create a new issue

If you spot a bug, want to request a new functionality, or have a question on how to use the module, please [search if an issue already exists](https://github.com/braniii/prettypyplot/issues). If a related issue does not exist, feel free to [open a new issue](https://github.com/braniii/prettypyplot/issues/new/choose).

### Solve an issue

If you want to contribute and do not how, feel free to scan through the [existing issues](https://github.com/braniii/prettypyplot/issues).

## Create a new pull request
### Create a fork

If you want to request a change, you first have to [fork the repository](https://github.com/braniii/prettypyplot/fork).

### Setup a development environment

=== "conda"

    ``` bash
    conda create -n pplt -c conda-forge python
    conda activate pplt
    python -m pip install -e .[all]
    ```

=== "venv"

    ``` bash
    python -m venv ./prettypyplot
    source ./prettypyplot/bin/activate
    python -m pip install -e .[all]
    ```

### Make changes and run tests

Apply your changes and check if you followed the codeing style (PEP8) by running
```bash
python -m tox -e lint
```
All errors pointing to `./build/` can be neglected, they are caused by my lazy approach of using no wildcards in the setup.

If you add a new function/method/class please ensure that you add a test function, as well. Running the test simply by
```bash
python -m tox
```
And please ensure that the coverage does not decrease. Otherwise the CodeCov bot will complain.

### Open a pull request

Now you are ready to open a pull request and wait on feedback.
