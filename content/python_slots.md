---
title: Reduce Python's memory use with slots
author: Marius Mather
date: 2024-05-29
Category: Python
Tags: python,programming
---

Python's classes are pretty flexible by default - you usually
initialize them with some attributes, but you can attach new
attributes to them after creation:

```python
class DefaultPoint:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

p = DefaultPoint(2, 3)
p.other = "Arbitrary values"
```

Allowing for these arbitary attributes means these classes
use more memory than what's needed to just store the initial attributes - they use
an internal dictionary that can accept new values. This extra memory
use usually doesn't matter too much, but if you're creating lots of instances,
it can add up.

If you just want to store known attributes, and use less memory to do it,
you can declare the **slots** that the class uses:

```python
class Point:
    __slots__ = ("x", "y")

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
```

Now the class only allows for storing `x` and `y`, and trying to add extra
attributes will raise an error.

```python
p = Point(2, 3)
p.other = "Not allowed!"
# AttributeError: 'Point' object has no attribute 'other'
```

If you use `dataclasses`, there's a shortcut to setting up the slots:

```python
@dataclass(slots=True)
class Point:
    x: int
    y: int
```

Comparing the memory use for a large number of instances, borrowing
the `get_size()` function from [wissam on StackOverflow](https://stackoverflow.com/a/38515297/1222578),
it looks like in this simple case, the instances with slots use 1/3rd of the memory:

```python
default_points = [DefaultPoint(2, 3) for i in range(10_000)]
slots = [Point(2, 3) for i in range(10_000)]
print(f"{get_size(default_points):,}")
# 1,525,332
print(f"{get_size(slots):,}")
# 565,176
```
