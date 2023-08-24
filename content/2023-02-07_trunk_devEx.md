title: Automating linting and error checking with Trunk
author: Januar Harianto
date: 2023-02-07
Category: misc
Tags: linting, error-checking, devEx, automation

## See Trunk in action in the `eeharvest` package [repository](https://github.com/Sydney-Informatics-Hub/eeharvest)

Use [Trunk] to check and monitor code prior to pushing it to production,
allowing you to catch issues quickly. It works like a local CI or pre-commit
hook for linting and formatting, but is **instantenous**. Best of all, it doesn't
force collaborators to install anything, and they may appreciate you for it.

With trunk you can replace:

- linters: e.g. `flake8`, `pylint`, `eslint`, `stylelint`, `shellcheck`,
  `markdownlint`
- formatters: e.g. `black`, `prettier`, `isort`, `shfmt`
- issue detection: e.g. `bandit`, `safety`, `mypy`
- [ErrorLens](https://marketplace.visualstudio.com/items?itemName=usernamehw.errorlens):
  in-line error reporting - installing this will result in "double" error reporting

All of the above are configured, installed and managed for you by Trunk, and
editable in a `.trunk.yaml` file.

## Lint

Trunk can lint your files as you type and shows you the errors inline:

<img src="{attach}images/trunk/flake8@2x.png" alt= “” width="500">

## Format

Enable automatic formatting on save - using `black`, `prettier`, or other
formatters of choice:

<img src="{attach}images/trunk/black_preview.gif" alt= “” width="800">

Trunk is available for free in _most_ circumstances.

[trunk]: https://trunk.io

## Check

When used in VS Code, Trunk can consolidate all issues in a "Check" sidebar:

<img src="{attach}images/trunk/check.png" alt= “” width="400">

## Other functionality

Trunk works with continuous integration workflows, accepts custom linters and
parsers, and has a robust CLI interface which allows developlers to allow
teammates to use its features without installing anything (if Trunk is commited
directly into the repo). Check out the documentation
[here](https://docs.trunk.io/docs).

**In most cases, a local install of Trunk is sufficient for routine linting and
error checks.** It's just so convenient.

## Installation

### VS Code (recommended)

Install via [VS Code
extensions](https://marketplace.visualstudio.com/items?itemName=Trunk.io). For
every new project, you will be asked if you want to initialise Trunk.

<img src="{attach}images/trunk/vscode_init_trunk.png" alt= “” width="300">

### Bash

If you use other editors, you can install Trunk via the command line:

```sh
curl https://get.trunk.io -fsSL | bash
```

Then, initialise trunk for a project by running the following command in the root folder:

```sh
trunk init
```

Use `trunk check` to run all linters, or `trunk fmt` to run all formatters. More
information ca be found in the documentation
[here](https://docs.trunk.io/docs/check-cli).
