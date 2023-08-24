title: Structure your data quickly and easily with Python dataclasses
author: Marius Mather
date: 2023-05-24
Category: Python
Tags: python,types,code

It can be a bit clunky to create a class in Python to store
data, as you need to define an `__init__` method and write some repetitive
code to assign all the attributes:

```python
class Animal
    def __init__(name: str, age: int):
        self.name = name
        self.age = age
```

Python's new `dataclass` (in the standard library from Python 3.7 onward) 
makes this a lot quicker and more efficient,
as it creates the `__init__` method for you automatically, all you
do is specify the types for the data:

```python
from dataclasses import dataclass

@dataclass
class Animal:
    name: str
    age: int

dog = Animal(name="Fido", age=5)
```

One of the big benefits of this is that your IDE/editor should
automatically pick up on the types of your data and warn you
when you're using it incorrectly. Using dataclasses can be
a good alternative to returning multiple results in a dictionary
or tuple, as it's easier to keep track of the different results.

If you want something a bit more advanced than `dataclasses`,
you can look at [Pydantic](https://docs.pydantic.dev/latest/),
which allows you to define data types in a similar way,
but also helps you convert data to and from other formats
like JSON.