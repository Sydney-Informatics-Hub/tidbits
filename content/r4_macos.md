---
Title: R 4.0 and Mac OS Issues - fixing data.table and fst
Date: 2020-05-25
Author: Marius Mather
Category: R
Tags: r,macos
---

The R maintainers have made some changes to how R is built
on Mac OS for R 4.0+: this should make some packages
like Stan easier to use, however it also seems to cause
issues with packages like `data.table` and `fst` that
use multi-threading. When loading these packages you may
see a warning about how they're only using single threads.

After checking multiple setup guides (e.g. 
[here](https://ryanhomer.github.io/posts/build-openmp-macos-catalina-complete)
and [here](https://github.com/Rdatatable/data.table/wiki/Installation)),
I was able to fix these issues using the following steps:

* Install the XCode command line tools:

```bash
xcode-select --install
```

* Install `llvm`, `gcc` and `libomp` through Homebrew:
  
```bash
brew install llvm gcc libomp
```

* Add the following to `~/.R/Makevars`:

```
XCBASE:=$(shell xcrun --show-sdk-path)
LLVMBASE:=$(shell brew --prefix llvm)
GCCBASE:=$(shell brew --prefix gcc)
GETTEXT:=$(shell brew --prefix gettext)

CC=$(LLVMBASE)/bin/clang -fopenmp
CXX=$(LLVMBASE)/bin/clang++ -fopenmp
CXX11=$(LLVMBASE)/bin/clang++
CXX14=$(LLVMBASE)/bin/clang++
CXX17=$(LLVMBASE)/bin/clang++
CXX1X=$(LLVMBASE)/bin/clang++

CFLAGS=-g -O3 -Wall -pedantic -std=gnu99 -mtune=native -pipe
CXXFLAGS=-g -O3 -Wall -pedantic -std=c++11 -mtune=native -pipe
CPPFLAGS=-isystem "$(LLVMBASE)/include" -isysroot "$(XCBASE)" 
LDFLAGS=-L"$(LLVMBASE)/lib" -L"$(GETTEXT)/lib" --sysroot="$(XCBASE)"

SHLIB_OPENMP_CFLAGS= -fopenmp
SHLIB_OPENMP_CXXFLAGS= -fopenmp
SHLIB_OPENMP_FCFLAGS= -fopenmp
SHLIB_OPENMP_FFLAGS= -fopenmp

FC=$(GCCBASE)/bin/gfortran
F77=$(GCCBASE)/bin/gfortran
FLIBS=-L$(GCCBASE)/lib/gcc/9/ -lm
```

After this, you should be able to successfully compile packages like
`data.table` with multi-threading support:

```r
install.packages("data.table", type = "source")
```

If your setup is working, loading `data.table` (or `fst`) should print
a message about how multiple threads are being used:

```
data.table 1.12.8 using 8 threads (see ?getDTthreads).
```
