Title: Counting zeros with dplyr summary tools
Date: 2020-08-05
Author: Henry Lydecker
Category: R
Tags: r,tidyverse

## The problem: losing data

The **dplyr** package has some very useful tools for creating summaries of your data through functions like dplyr::count(), as well as the more powerful dplyr::summarise() function using the n() argument.
However, by default these functions do something that is not always wanted: they don't count zeros. 
This is not ideal in many situations, as zero is a measurement.

## The solution: `.drop=FALSE`

The solution to this problem is relatively simple. With dplyr::count(), you can find the solution in the documentation straight away:

```
count(something) # zero is not counted, because by default .drop = TRUE

count(something, .drop = FALSE) # by changing this argument, we are now counting zero
```


