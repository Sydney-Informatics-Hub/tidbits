title: Standardised Python testing with Tox and `tox-conda`
author: Januar Harianto
date: 2023-02-07
Category: Python
Tags: automation, python, unit-testing, devops

[Tox](https://github.com/tox-dev/tox) is a great too that standardises package
building, testing, linting and CI-integration for Python projects. As not
everyone builds Python packages, this article will focus on automatic **unit
tests** for any python code.

Installing tox is as simple as:

```sh
pip install tox
```

Or if you use conda/mamba:

```sh
conda install -c conda-forge tox
```

## Tox and `eeharvest`

The [`eeharvest`](https://github.com/Sydney-Informatics-Hub/eeharvest) package
uses Tox to automate a bunch of things:

1. building the package
2. running tests using `pytest` in multiple environments
3. checking code coverage
4. publishing to PyPI

If configured properly, the first four actions can be done in a single command:

```sh
tox
```

Publishing the package to PyPI is as simple as:

```sh
tox -e publish -- --repository pypi
```

Below is a preview of what happens when using tox for unit testing. If you look
closely, tox is running unit tests on Python versions 3.8 to 3.11 (6
environments in total), and then publishing the coverage for each environment:

<img src="{attach}images/tox/tox_action.gif" alt= “” width="600">

### Configuration

Tox works by looking at a `tox.ini` file in the root of the project. That's it.
A single file.

A simple configuartion for two test environments, Python 3.8 and 3.11, can be
generated with the following configuration settings in the file:

```ini
[tox]
requires =
    tox>=4
env_list = py{38,311}
requires = tox-conda

[testenv]
description = Invoke pytest to run automated tests
setenv =
    TOXINIDIR = {toxinidir}
extras =
    testing
deps =
    pytest>=7
    pytest-sugar
conda_deps =
    geedim
conda_channels=
    conda-forge
conda_install_args=
    --override-channels

commands =
    pytest {posargs:tests}
```

Note that the above config requires use of `tox-conda`, which can be installed
via mamba/conda:

```py
mamba install -c conda-forge tox-conda
```

Tox will automatically configure conda environments, because `requires =
tox-conda` is set. For each environment specified in `env_list`, it will install
dependencies specified in `conda_deps` and `deps` (pip dependencies), and then
run tests in your tests folder.

For more information on configuring tox, see the [official
documentation](https://tox.wiki/en/latest/user_guide.html).
