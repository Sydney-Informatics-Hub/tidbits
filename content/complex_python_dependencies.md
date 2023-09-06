---
title: Handling complex Python dependencies: an opinionated guide
author: Marius Mather
date: 2023-09-06
Category: Python
Tags: python,conda
---

Python dependency management has improved over the years, but you
can still run into issues, particularly when using machine
learning libraries like **Torch** or **TensorFlow** that have
compiled or non-Python dependencies.

In my opinion, [conda](https://docs.conda.io/en/latest/) is very
good at handling data science/machine learning projects with
these complex dependencies. The conda repositories don't just contain
Python packages: they also include C libraries, compiled binaries, and
all the other external dependencies that packages like `torch` depend on.
`conda` also tries to handle installing compatible versions for these non-Python dependencies.

Note that you only get these benefits of `conda` if you install packages from the
conda repositories, because conda packages are different to the standard Python packages
available on [PyPI](https://pypi.org/). If you use `conda` to create an environment but install
via `pip` or a `requirements.txt`, you don't get `conda`'s pre-compiled binary packages.

My personal tips for using `conda` in complex projects are:

* Use an `enviroment.yml` file to record your dependencies
* Use the `conda-forge` channel - this has a lot more packages
  than the default conda repository
* Check if the packages you need are available through conda first.
  If not, you can install them through `pip` (while still specifying them in `environment.yml` - see below)
* Don't pin packages to specific versions unless absolutely necessary - this is definitely more in the realm of opinion,
  but I think very specific version requirements make it harder to update packages in future. I would recommend pinning most
  packages to the current major version, e.g. `dependency>=1.5.0,<2.0`, unless you have a specific reason to pin to a minor
  version.

## You can still install pip packages! (if they're not in `conda-forge`)

Before installing any packages via `pip`, you should:

* Search conda (including the `conda-forge` channel) to see if the package is there:
  `conda search -c conda-forge <package>`
* See if there's another channel that has the package available - there's a dedicated
  `pytorch` channel, and `bioconda` has a lot of bioinformatics tools.

To include `pip` packages in your conda environment, you need two entries for `pip`

* One that just installs the `pip` package itself
* A nested list that specifies all the packages you want to install

For example:

```yml
dependencies:
  - python=3.10
  - pip
  - pip:
      - ols-py==0.2.5
```

## Example yml file for a complex project

This is one of my projects that includes multiple complex dependencies, all of which
I can install using a single conda environment file.

* A number of Python packages, some of which are installable via conda, some not - where possible, I install them from `conda`
* Machine learning libraries like `PyTorch`
* Bioinformatics tools and libraries, which I can install through the `bioconda channel`

```yml
name: my_project
channels:
  - defaults
  - conda-forge
  - bioconda
dependencies:
  # Python libraries
  - python=3.10
  - django=3.2.16
  - django-ninja>=0.20.0,<1.0
  - numpy
  # Bioinformatics libraries/tools
  - bioconda::htslib
  - bioconda::pysam
  - bioconda::hgvs
  # cython makes installing htslib easier
  - cython
  # Machine learning libraries
  - pytorch>=1.13.1,<1.14.0
  - transformers==4.24.0
  - accelerate
  - pip
  # Libraries not available through conda
  - pip:
      - ols-py==0.2.5
      - django-environ>=0.9.0,<1.0
```


