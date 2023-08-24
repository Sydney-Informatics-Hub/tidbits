Title: mamba: a fast replacement for conda
Date: 2021-04-22
Author: Marius Mather
Category: Python
Tags: python,conda,package-management

If your `conda` environment is taking a long time to solve (or
failing to solve altogether), you might want to try [mamba](https://github.com/mamba-org/mamba),
which reimplements `conda` in C++ with an improved dependency
solving algorithm.

To install in your existing conda setup (from their instructions [on Github](https://github.com/mamba-org/mamba))

```shell
conda install mamba -n base -c conda-forge
```

Then you should be able to run `mamba` instead of `conda` for
commands like creating environments:

```shell
mamba env create -n my_project --file environment.yml
```

It's not a complete replacement for `conda` (yet), you still have to use
`conda activate` to activate your environments, but it seems
to greatly speed up installing packages and creating environments.

The same developers have also created [rhumba](https://github.com/mamba-org/rhumba),
a similar package manager for R - this might also be worth looking
at for creating reproducible R environments.

