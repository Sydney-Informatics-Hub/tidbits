title: Use logging instead of print
author: Marius Mather
date: 2022-06-06
Category: python
Tags: python,development

Like a lot of people, I'm guilty of using `print()` to debug
my code. While it's a good idea to use a proper debugger,
it can also be good to have your programs log useful
information as they run, particularly if they're going
to run on a server relatively unsupervised. That's where
Python's [logging](https://docs.python.org/3/library/logging.html)
module comes in. It's best to use `logging` instead
of `print` right from the start of a project, so keep
it in mind for your next one!

At the most basic level, `logging` lets you set the importance
level of each message you're sending. The levels (in order of importance) are:

- DEBUG
- INFO
- WARNING
- ERROR
- CRITICAL

To log each kind of message, just use the equivalent function from `logging`:

```python
logging.debug("Log a debug message")
logging.warning("Log a warning")
# etc.
```

When running your code, you can set the log level (using a command line
argument, environment variable, config file, etc.), and only messages
of that importance or higher will be shown:

```python
logging.basicConfig(level=logging.INFO)
logging.debug("This won't be shown")
logging.info("Anything at info level or higher will be logged")
```

The benefit of this is you can have your programs show a lot of information
on what they're doing through `debug` messages, without making
the output too noisy for regular use. If you find yourself going
back through your code removing `print()` statements once it's finished,
consider using `logging` instead.

Going further, the `logging` module has lots of useful functionality like:

- Logging to a file instead of/as well as the console - and easily switching
  between these
- Automatically including context like the current Python module and line number in messages
- Running multiple loggers with different settings.

See [this RealPython tutorial](https://realpython.com/python-logging/) for info
on some of these.

The closest equivalent in R seems to be the [logger](https://github.com/daroczig/logger/)
package, which is inspired by Python's logging.
