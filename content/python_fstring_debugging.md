---
title: Quick debugging with Python f-strings
author: Marius Mather
date: 2024-02-14
Category: Python
Tags: python
---

You should probably set up [logging]({filename}/python_logging.md) for your Python code,
for any important information you need to keep track of. But, when you
need to do a little bit of "print debugging", Python's **f-strings**
are a really convenient option.

**F-strings** allow you to include variables directly in strings, without using
methods like `str.format()`:

```python
x = 18
print(f"Total apples: {x}")
# Total apples: 18
```

Even better for debugging, if you add `=` to the end of the variable, you
get both the variable name and value printed, making it very easy to quickly
keep track of what's happening:

```python
y = x + 5
z = y * 2
print(f"{y=}, {z=}")
# y=23, z=46
```

There are lots of other useful formatting tricks you can do with f-strings,
like formatting large numbers with commas:

```python
large_n = 1048213
print(f"{large_n:,}")
# 1,048,213
```

See this [cheat sheet](https://fstring.help/cheat/) for more.
