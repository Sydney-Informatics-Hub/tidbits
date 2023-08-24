Title: Design patterns (Part 1)
Date: 2021-09-28
Author: Sergio Pintaldi
Category: Python
Tags: Python, Software Engineering, Design, Architecture

# Design Patterns (Part 1): What? Why?

## What is a Design Pattern

> In software engineering, a software design pattern is a general, reusable solution to a commonly occurring problem within a given context in software design.
source: [Wikipedia](https://en.wikipedia.org/wiki/Software_design_pattern)

## Why use Design Patterns

* Tested and adopted by the wider software community
* Re-usable pieces of code
* Common language to solve problems in software design and development
* ...

Sources:
* [Wikipedia - Software Design Pattern](https://en.wikipedia.org/wiki/Software_design_pattern)
* [Refactoring - Design Patterns](https://refactoring.guru/design-patterns)

# Design Patterns in `Python`: an example that I used in my projects

## The `Singleton` Design Pattern

> Ensure a class has only one instance, and provide a global point of access to it.
source: [Wikipedia](https://en.wikipedia.org/wiki/Singleton_pattern)

### Code

```python
class MySingletonClass(object):
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super(MySingletonClass, self).__new__(cls)
        return cls.__instance

    def __init__(self, some_argument):
        self.some_argument = some_argument
```

or another variant:

```python
class MySingletonClass(object):

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, __instance):
            cls.__instance = super(MySingletonClass, self).__new__(cls)
        return cls.__instance

    . . .
```

Singleton to inherit from (multiple classes can inherit without getting confused):

```python
class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = (
                super(Singleton, cls).__call__(*args, **kwargs)
            )
        return cls._instances[cls]


class MySingletonClass(Singleton):
    """docstring for MySingletonClass"""
    def __init__(self, arg):
        self.arg = arg
```

there are many more definitions if you [Google it](https://www.google.com/search?channel=fs&client=ubuntu&q=python+singleton).

### Usage: How do I know that is really a Singleton?

Here below I demonstrate how to check if you did it right.

```python
class MyClassSingleton(object):
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super(MyClassSingleton, cls).__new__(cls)
        return cls.__instance

    def __init__(self, arg1, arg2):
        self.arg1 = arg1
        self.arg2 = arg2
```

```python
MyClassSingleton(1, 2)
```

    <__main__.MyClassSingleton at 0x7feac43f2c40>


```python
class1 = MyClassSingleton("this", "that")
class2 = MyClassSingleton("this", "that")
```

```python
class1 is class2
```

    True

```python
hex(id(class1)), hex(id(class2))
```

    ('0x7feac43f2c40', '0x7feac43f2c40')

```python
class MyClassNotSingleton(object):

    def __init__(self, arg1, arg2):
        self.arg1 = arg1
        self.arg2 = arg2
```

```python
class1 = MyClassNotSingleton("this", "that")
class2 = MyClassNotSingleton("this", "that")
```

```python
class1 is class2
```

    False

```python
hex(id(class1)), hex(id(class2))
```

    ('0x7feac440cf40', '0x7feac440cb50')

### How did I use it?

* creating connection to database
* creating connection Dask cluster: no need to pass it through functions, but just create an instance of it to return always the same object

But can be used also for:

* get some data from something only once and save it as attribute in a class
* ... (google for more examples)

## Coming soon ...

* Design Patterns Part 2: more design patterns that I used
* Design Patterns in R

## More Reading

* [Medium - The 7 Most Important Software Design Patterns](https://medium.com/educative/the-7-most-important-software-design-patterns-d60e546afb0e)
* google "Design Patterns in ..."
