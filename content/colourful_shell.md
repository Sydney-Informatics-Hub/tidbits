title: Add some colour to your shell: modern terminal tools
author: Marius Mather
date: 2020-06-16
Category: Misc
Tags: shell,terminal,zsh

While I'm pretty comfortable with basic shell commands, I like
the convenience of features like syntax highlighting. Lately
I've discovered a few replacements for common shell commands
that add an extra bit of colour:

## bat: cat with syntax highlighting

`bat` is a drop-in replacement for `cat` that adds syntax highlighting
and line numbers by default - great for when you want to check
the contents of a script:

![Syntax highlighting with bat]({attach}images/colourful_shell/bat_screenshot.png)

On Mac you can install it via Homebrew:

```bash
brew install bat
```

## exa: ls with syntax highlighting

On a (very) similar note, `exa` is a drop-in replacement for `ls` that adds
a bit more colour. By default, it just adds some colouring for different
file types:

![exa default output]({attach}images/colourful_shell/exa_default.png)

When used with options like `-l` it adds some colour to the structured
information, e.g. the permissions:

![exa with -l]({attach}images/colourful_shell/exa_permissions.png)

Again, install with Homebrew:

```bash
brew install exa
```

## ripgrep: an easier grep

I'm very bad at using `grep` -  I can never remember whether the
file or the pattern goes first. [ripgrep](https://github.com/BurntSushi/ripgrep) 
makes `grep` more convenient:
by default you can just give it a pattern and it will search the
current folder recursively (automatically skipping hidden files and files
in your `.gitignore`).

You get nice colourful output with the matches highlighted:

![ripgrep output]({attach}images/colourful_shell/ripgrep.png)

```bash
brew install ripgrep
```

## Lots more

I've only covered tools that I've been using regularly - there
are plenty more out there if you want to improve your shell.
There's a long list [here](https://github.com/alebcay/awesome-shell),
and other fun tools like [asciinema](https://asciinema.org/) which
lets you record gifs/videos of your shell sessions.