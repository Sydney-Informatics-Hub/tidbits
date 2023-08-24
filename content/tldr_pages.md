title: tldr: A short, sweet, alternative to man pages
author: Marius Mather
date: 2020-07-13
Category: Misc
Tags: shell,terminal,git

If you want to get something done in your shell but don't
want to scour through a whole `man` page looking
for the right combination of options, `tldr` might have
answers for you.

`tldr` is a shell tool (installable via `brew install tldr`)
that gives short, human-readable examples of common shell
commands, as an alternative to man pages. For example,
running `tldr ls` gives:

![tldr ls output]({attach}/images/tldr_pages/ls_output.png)

`tldr` also has specific pages for individual `git` commands,
with examples of how to use it in specific situations.
e.g. for `tldr git rebase`:

![tldr git output]({attach}/images/tldr_pages/git_output.png)