title: Modernize your Python code with type annotations
author: Marius Mather
date: 2021-11-24
Category: python
Tags: python,types,development

Python has supported optional type annotations since
Python 3.6, like:

```python
# Specify argument and return types
def add(x: int, y: int) -> int:
    return x + y
```

All currently supported Python versions support them
now, so you can start adding them to your code
without breaking anything.

Type annotations are entirely optional and are basically
ignored by the Python compiler, so you won't break
your code by including them. However, once you start adding
them to your code you should find that your editor/IDE
can give you better autocompletion for object methods (because it
can determine their type), and can catch errors in how you're
using your functions:

![Type error checking in VS Code]({attach}images/python_type_annotations/type_error.png)

For more detailed and rigorous checking of your code-base,
you can use tools like [mypy](http://mypy-lang.org/), which scans your code-base to
ensure all types are consistent.

Annotation tools can be found in the `typing` module in the standard library.
Some of the most common useful type annotations include using the `Optional` annotation
to document when an argument can be `None`:

```python
from typing import Optional

def append_data(value: float, current_data: Optional[list] = None):
    if current_data is None:
        current_data = []
    current_data.append(value)
```

Or specifying the types for your nested data structures:

```python
# In newer versions of Python (>= 3.9), you can just use
# list or tuple directly
from collections import defaultdict
from typing import Dict, List, Tuple

def get_total_scores(scores: List[Tuple[str, int]]) -> Dict[str, int]:
    totals = defaultdict(int)
    for person, score in scores:
        totals[person] += score
    return totals

get_total_scores([
    ('Alice', 3), ('Bob', 2), ('Alice', 1)
])
```
