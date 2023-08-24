---
Title: Generating an automatic index for Github Pages
Date: 2020-05-14
Author: Marius Mather
Category: Python
Tags: python,github,github-pages
---

The output you deliver to clients might include
multiple reports, e.g. HTML files generated from
RMarkdown. In order to display these using Github
Pages, it's useful to create an index that links
to them, so clients can easily access all reports
via a landing page.

I found this Python script [on Stack Overflow](https://stackoverflow.com/a/39402604/1222578)
(written by user Matthew Brett)
which scans a directory (e.g. the `docs/` directory that Github Pages
uses), and generates the index:

```python
""" Build index from directory listing

make_index.py </path/to/directory> [--header <header text>]
"""

INDEX_TEMPLATE = r"""
<html>
<body>
<h2>${header}</h2>
<p>
% for name in names:
    <li><a href="${name}">${name}</a></li>
% endfor
</p>
</body>
</html>
"""

EXCLUDED = ['index.html']

import os
import argparse

# May need to do "pip install mako"
from mako.template import Template


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("directory")
    parser.add_argument("--header")
    args = parser.parse_args()
    fnames = [fname for fname in sorted(os.listdir(args.directory))
              if fname not in EXCLUDED]
    header = (args.header if args.header else os.path.basename(args.directory))
    print(Template(INDEX_TEMPLATE).render(names=fnames, header=header))


if __name__ == '__main__':
    main()
```

If you have Github Pages set up to use the `docs/` directory,
then you should be able to generate an index for your project
with:

```bash
make_index.py docs/ --header "My Project Name" > docs/index.html
```