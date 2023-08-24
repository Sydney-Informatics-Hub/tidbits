Title: Pandas dataframe to Markdown
Date: 2020-04-17
Author: Sergio Pintaldi
Category: Python
Tags: Python, Pandas, GitHub, Markdown

# The Problem
In building up code and tracking the bugs, it is extremely useful posting the `traceback` in a GitHub issue. The problem is that when we are dealing with pandas dataframes, it is not easy to convert the df into a markdown. Given the following df:

```python
import pandas as pd

df = pd.DataFrame([['a',1],['b',2],['c',3]], columns=['letters', 'numbers'])
```

You need to incorporate it into something like this:

<!-- language: lang-none -->

    ```python
      letters  numbers
    0       a        1
    1       b        2
    2       c        3
    ```

to have the following output:

```python
  letters  numbers
0       a        1
1       b        2
2       c        3
```

# The solution
Starting from version `1.0` Pandas now inlude a `to_markdown()` method that would make the things easier for us. See below:

```python
>> print(df.to_markdown())
|    | letters   |   numbers |
|---:|:----------|----------:|
|  0 | a         |         1 |
|  1 | b         |         2 |
|  2 | c         |         3 |
```

Then copy and paste it in a GitHub Issue:

![]({attach}images/pandas-to-markdown/pandas-df-to-markdown.png)
