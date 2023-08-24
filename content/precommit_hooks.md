title: git pre-commit hooks: check or style your code with every commit
author: Marius Mather
date: 2021-07-07
Category: git
Tags: git,python,black

You can use tools like [black](https://github.com/psf/black) to automatically
style your Python code in a consistent way. However, if you're just running
it manually, you have to remember to run it regularly, and you'll probably
end up with lots of git commits that are just "Style fixes".

[pre-commit](https://pre-commit.com/) uses 
[git hooks](https://git-scm.com/book/en/v2/Customizing-Git-Git-Hooks) 
to run different tools before each git commit. A hook that runs
`black` allows you to automatically style any new code before it gets 
committed.

To set up `pre-commit`, install the `pre-commit` package into
your Python environment, and create a `.pre-commit-config.yaml`
file. The config file for running `black` looks like:

```yaml
repos:
-   repo: https://github.com/psf/black
    rev: 21.6b0
    hooks:
    -   id: black
```

Once you've created the config file you can run `pre-commit install`
and the hooks will be set up. If you have existing code you
can run `pre-commit run --all-files` to style it all.

You can also use commit hooks for automated testing with `pytest`
(you can run commits at each push rather than each commit if
this would be too slow), fixing minor whitespace errors, 
or custom tests you've created. There's a big list of
available hooks [here](https://pre-commit.com/hooks.html) to
get you started.