Title: Easy delivery of local R Shiny dashboards
Date: 2021-01-11
Author: Henry Lydecker
Category: R
Tags: R, Shiny

Sometimes we don't need to deploy R Shiny dashboards to a server, and it is ok to just run them locally. 

In these cases, we can make it easier for clients and users to run dashboards we create for them using a nifty function: **shiny::runGithub()**.

Here's an example of how to use this function, shamelessly borrowed from the [documentation](https://www.rdocumentation.org/packages/shiny/versions/0.9.0/topics/runGitHub) for this function:

```
runGitHub("shiny_example", "rstudio")

# Can run an app from a subdirectory in the repo
runGitHub("shiny_example", "rstudio", subdir = "inst/shinyapp/")
```

When you run this function, it will check if you have the dependencies for the dashboard installed, and automatically install them if you don't have them.
