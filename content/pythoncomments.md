---
Title: The world's shortest tidbit: use #%% in Python scripts
Date: 2021-11-15
Author: Darya Vanichkina
Category: Python
Tags: Code,git
---

# The world's shortest tidbit



I don't think this is really worthwhile as a tidbit, as it's (1) very short, and (2) very obvious - once you know about it. 

But this is a productivity lifehack that makes it much easier to use Python for data science, through both VSCode and PyCharm, kind of how easy R is to use via RStudio. 

The tidbit is:

**If you break up the code in your `.py` script with comments of the format `#%%` this will get both VSCode and PyCharm to recognise the code below them, until the next `#%%`, as a code cell (what R calls a "code chunk").**

This has the benefits:

- You can execute code cell-by-cell (and not just line by line) using keyboard shortcuts. For example, in the image below, I used `shift-Return` to execute all of the imports at once.
- When live-debugging and working on your code you can get a jupyter-notebook-like interface (aka console, for the R users) on the right, where you can type extra commands that you want to use to develop and prototype your code as you go along. 
- Because your actual code is stored in a `.py` file, it is nicely amenable to version control with git - making it like `Rmd` files in this regard. Conversely, jupyter notebook output is also stored with the notebook, so can look like a binary mess with git - although GitHub does try to ameliorate this problem somewhat.

So there really are heaps of benefits - and no drawbacks I've been able to see - for using `# %%` in your Python code.



![]({attach}images/20211115_pythoncomments.jpeg)



