# SIH Tech tidbits blog

The aim of this blog is to act as a simple repository for tech
tidbits that we want to share with other SIH team members.

If you want to submit a new tidbit, you can put together
a Markdown file explaining your tidbit (hopefully with
some short code examples).  The site will be built automatically
when you commit to `main` (so maybe use a pull request for any draft
posts).

Markdown files for posts/tidbits go in the
`content/` directory. It would be great if you could
also include some metadata at the top of the file, filling
in the `Title`, `Date`, `Author`, `Category` and `Tags` fields. Posts
can only have one `Category`, but multiple `Tags`.

```yaml
Title: fst: A very fast file format for R
Date: 2020-01-30
Author: Marius Mather
Category: R
Tags: r,file-formats,large-data
```

Attaching images uses some Pelican-specific syntax: put the images in the `content/` folder along
with the Markdown files, put `{attach}` at the start of the path, and then specify the
rest of the path **relative to the content folder**, e.g.:

```
![]({attach}images/deploy_shiny_app/runapp_rstudio.png)
```

You can include images that are hosted elsewhere on the web using the regular Markdown image syntax.

## RMarkdown

The blog now supports (semi-)automated conversion of RMarkdown files. To create a post from an
RMarkdown file: 

* Put your RMarkdown files in the `rmd_content/` folder, along with any data files they need. 
* Put metadata like `Category:` and `Tags:` in the YAML header at the top of the RMarkdown script,
  along with standard fields like `Title:`, `Author:` and `Date:` (although Pelican doesn't seem
  to like it when you use quotes `"` around these fields)
* Put any external images you're using in `rmd_content/images/` and include them using `knitr::include_graphics()`
  (images for plots produced by RMarkdown should be handled by the conversion script you don't
  need to do anything extra)

Running the `convert_rmarkdown.R` script should render any new RMarkdown files into
plain Markdown and copy them to the `content/` folder, along with their images.

## Technical details

The blog is built with [Pelican](https://blog.getpelican.com/),
a basic static site generator implemented in Python. We use
the `tag_cloud` and `tipue_search` plugins to add some basic
searchability.

We use GitHub Actions to automatically build and deploy the site,
so you don't need to install Pelican unless you want to preview
your content locally.

### Installing/testing locally

The dependencies are managed with [Poetry](https://python-poetry.org/).
Once you've installed Poetry, you should be able to install
all the dependencies into a dedicated virtual environment, and
then activate that environment, with:

```bash
poetry install
poetry shell
```

You can preview the site using

```bash
pelican --listen --autoreload
```

and opening `http://localhost:8000` in your browser.

To rebuild the published version of the site, run:

```bash
pelican -s publishconf.py
```

Unlike Jekyll, Github Pages does not automatically build sites
using Pelican, so to have the pages show up, we need to build
it ourself and commit the contents of the `docs/` folder to the repo.
MM will rebuild the output when necessary.
