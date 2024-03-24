title: Late Binding in Python
author: Hamish Croser
date: 2024-03-25
Category: python
Tags: python,code,debugging

In Python, a function takes the latest value assigned to a variable rather than the value assigned at definition time. This is known as late binding.

This is usually intuitive but can be confusing in some circumstances, e.g. lambdas in a loop:

```python
funcs = [lambda: i for i in range(3)]
for f in funcs: print(f())
```
The above will output:
```
2
2
2
```
<br>

One way to fix the variable's value at definition time is to include it as a default argument, like so:

```python
funcs = [lambda i=i: i for i in range(3)]
for f in funcs: print(f())
```
The above will output:
```
0
1
2
```