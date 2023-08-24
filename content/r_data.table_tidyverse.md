Title: Getting data.table to work with the tidyverse
Date: 2021-05-24
Author: Jazmin Ozsvar
Category: R
Tags: R, tidyverse, data.table, dtplyr, tidytable

### data.table

**data.table** is a fast, efficient data format built upon data frames/tibbles designed to work with large data sets. It comes with its own set of syntax and chaining commands which are similar to those of Python. However, if you simply can't bear to code without the pipe operator (%>%) then here's are some workaround options for you!

### dtplyr

**dtplyr** is a Hadleyverse package that allows you to apply dplyr syntax to data.tables. This is done by converting a data.table into a lazy data frame in a single simple step:

```
# Load packages
library(dtplyr)

# Turn your data.table into a lazy data frame
a_lazy_df <- dtplyr::lazy_df(a_data_table)
```

Voila! Applying lazy_df() will allow you to use tidyverse verbs with your data.table. However, there is one more step required to actually view the results. This is because dtplyr saves the steps to obtain the result rather than writing out the result itself (i.e. lazy evaluation). This is so that when the lazy data frame operations are called they are executed only when required. 

```
# Apply some verbs and create a tibble
a_tibble <- a_lazy_df %>%
    filter(favourite_syntax == "tidyverse") %>%
    as_tibble()
    
# We can also use as.data.table() or as.tibble()
```

There is a small performance tax according to Hadley, however, it is almost on par with data.table itself. So if you need to use data.table but don't want to use its syntax, dtplyr is the package for you! For more information, check out: <https://www.tidyverse.org/blog/2019/11/dtplyr-1-0-0/> 


### tidytable

**tidytable** allows for the use of other useful tidyverse functions, not just those from dplyr, but allowing mapping with purrr and extra tidying using tidyr. Tidytable takes the tidyverse functions and puts a dot within their name to indicate they are for use with data.table, e.g. mutate() becomes mutate.(). This makes application very simple:

```
mtcars_dt %>%
  tidytable::summarise.(
    mean_disp = mean(disp),
    mean_hp = mean(hp),
    count = n(),
    .by = cyl
  ) %>%
  tidytable::arrange.(count)
```

To look at the full list of functions, have a look at: <https://markfairbanks.github.io/tidytable/reference/index.html>


### Microbenchmarking

Don't believe the above packages are speedy? Here's a comparison of the following codes using the mtcars dataset:


```

# Create the objects required
mtcars_dt <- as.data.table(mtcars)
mtcars_lazy_dt <- lazy_dt(mtcars_dt)

# data.table
mtcars_dt[, .(mean_disp = mean(disp),
             mean_hp = mean(hp),
             count = .N), by = cyl][order(count)]

# data.frame
mtcars %>%
   dplyr::group_by(cyl) %>%
   dplyr::summarise(
     mean_disp = mean(disp),
     mean_hp = mean(hp),
     count = n()
   ) %>%
   dplyr::arrange(count)
    
# dtplyr
mtcars_lazy_dt %>%
    dplyr::group_by(cyl) %>%
    dplyr::summarise(
      mean_disp = mean(disp),
      mean_hp = mean(hp),
      count = n()
    ) %>%
    dplyr::arrange(count) %>%
    data.table::as.data.table()
    
# tidytable
mtcars_dt %>%
    tidytable::summarise.(
      mean_disp = mean(disp),
      mean_hp = mean(hp),
      count = n(),
      .by = cyl
    ) %>%
    tidytable::arrange.(count)
```

We can see that data.table is the fastest, as expected, and the data.frame operations are the slowest. tidytable lags a little behind dtplyr in terms of performance, but is still considerably faster than data.frame.

| Package | Mean time (ms) |
| --- | ----------- |
| data.table | 0.6823924 |
| data.frame | 4.1101719 |
| dtplyr | 1.9016071 |
| tidytable | 2.5038907 |
