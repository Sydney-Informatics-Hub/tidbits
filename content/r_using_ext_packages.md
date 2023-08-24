Title: Using external packages in your R package
Date: 2020-08-07
Category: R
Tags: R, packages, roxygen2

If you're building a package in R it's highly likely that you'll have to eventually rely on functions from external packages (unless you enjoy rebuilding the wheel, or can't/don't need to). This tidbit is a quick summary of my experiences with using external R packages within my own (or clients') packages. 

So, let's say you've set up an R package, have some code, and want to use functions from external packages to write your code.


## DESCRIPTION

> "To depend, or not to depend, that is the question."

The first thing you need to do is consider how heavily your code relies on external functions. You will need to state the type of dependency in the `DESCRIPTION` file in the root directory of your package. This will dictate whether or not external packages are installed/loaded/attached at the same time as your package is installed/loaded.

**Depends:** if your package extensively relies on another package, it is appropriate to list that package under this category. Packages listed here will be loaded and attached with `library()` when your package is loaded. It's a good idea to state what version of the package is required, as you may not want just any version of these packages installed.

**Imports:** if your package relies on a number of functions from a package throughout the code, then list it under Imports. These packages will be installed and loaded along with your package but aren't attached with `library()`. Adding a package to Imports is like a courtesy to your end users so that the installation is done for them.

**Suggests:** if you use other functions/packages sporadically throughout your code  - perhaps in one or two places or in a function that will not be commonly used - then pop them into Suggests. These packages will require manual installation by the end user.

*The difference between attaching and loading a package is that loading a package makes the package available to the R session but its functions won't be available to the global environment, whereas attaching a package means its functions are available to the global environment.*

Want to add a package to `DESCRIPTION?` No worries. Rather than adding it by hand and potentially making a mistake, use:

```
library(usethis)
usethis::use_package("package", "dependency type")
```

## NAMESPACE and specifying imports

> "A function by any other name would (not) smell as sweet."

Now that we understand the point of `DESCRIPTION`, let's talk about how to actually import functions and how this relates to `NAMESPACE`. `NAMESPACE` is also located in the root directory and tells us which functions are being exported or imported for a particular package. You shouldn't have to write anything into `NAMESPACE` manually because `roxygen2` will basically handle things for you so long as you've written your function with the appropriate tags.

**Depends:** when you're using a function from a package in Depends, you generally don't need to specify anything other than the function in your code (this is because the package is attached along with your package). I have had a handful of instances where this didn't hold true though, oddly enough, in which case you can call it via the methods for Imports (below).

**Imports:** you should load functions from packages from these groups with `@importFrom package function` or using `package::function`. `@importFrom` is incredibly useful as it allows you to load specific functions rather than the entirety of a package. It will write an importFrom() line into your Namespace specifying the function/package that is loaded and accessible to the functions of your package. It is also slightly (5 us) faster than using `::`. That being said, if you have a case where two functions from different packages have the same name, `@importFrom` won't save you, so you should use `::` to explicitly state which packages the functions are from.

**Suggests**: since these packages aren't actually installed, it is best practice to include `ifrequireNamespace()` within your function to alert the user that they need to install these packages before they can use your function, as below:

```
my_fun <- function(x) {
  if (!requireNamespace("package", quietly = TRUE)) {
    stop("Package \"package\" needed for this function to work. Please install it.",
      call. = FALSE)
  }
}
```

It's then good to call the external function from the package with `::` to be sure it loads correctly after the package in question has been installed and loaded.


## Summary table

> "I wasted time and now doth time waste me."

For an even more TL;DR version of this tidbit.

| Category | When to use?                          | Installs with your package? | Loads with your package?           | Function use                                      |
|----------|---------------------------------------|-----------------------------|------------------------------------|------------------------------------------------------------|
| Depends  | If your package uses a package A LOT  | Yes                         | Loaded and attached with `library()` | Can use as is, but if that doesn't work then use`@importFrom` or `::`                                          |
| Imports  | For packages that are used less then A LOT but more than sporadically | Yes                         | Loaded but not attached            | `@importFrom` or `::`                                          |
| Suggests | For sporadically used packages        | No                          | No                                 | `::` but only after added `!ifrequireNamespace` |
