title: Better autocompletion in Jupyter Lab
author: Marius Mather
date: 2021-02-12
Category: Python
Tags: python,jupyter,tools

Autocompletion of variable names in Jupyter Lab (or Notebook)
can be frustratingly inconsistent. For a smoother development
experience, the [`jupyterlab-lsp`](https://github.com/krassowski/jupyterlab-lsp)
extension provides better completions using the same
language servers as Visual Studio Code.

Note that this is only available in Jupyter Lab 3+, not Jupyter Notebook.

To install it in your conda environement, run:

```bash
conda install -c conda-forge 'jupyterlab>=3.0.0,<4.0.0a0' jupyterlab-lsp python-language-server
```

(or add the packages to your `environment.yml` file).

## Autocompletion

To use regular Tab-completion, start typing in a code cell, hit `Tab`, and
you should get a list of possible completions, including type
information and documentation:

![Autocompletion]({attach}images/better_jupyter_autocompletion/tab_completion.png)

To access documentation once the code's been written, you can hover
your mouse over a function/class call and hit `Ctrl`:

![Documentation]({attach}images/better_jupyter_autocompletion/quick_docs.png)

## Style tips

The extension also offers some features similar to Visual Studio Code
or Python IDEs, like highlighting poor style or possible errors
in your code (these can be disabled):

![Error highlighting]({attach}images/better_jupyter_autocompletion/errors.png)

(code examples from <https://nbviewer.jupyter.org/url/norvig.com/ipython/Probability.ipynb>)