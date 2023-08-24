Title: fst: A very fast file format for R
Date: 2020-01-30
Author: Marius Mather
Category: R
Tags: r,file-formats,large-data

The [fst package](https://www.fstpackage.org/) allows very fast reading and
writing of data from R - much faster than `.rds` files. This can save
a lot of time when dealing with medium to large datasets.

By default it uses less compression than `.rds`, but even with `compress = 100`, it produces similar file sizes to `rds` and is still much faster.

It can also read arbitrary rows and columns from a file, so you can:

* Save time by only reading in the columns you need from a file
* Save memory by only reading one **chunk** from the file at a time
  and processing it (you do need a processing task that can be
  done separately on each chunk)

A simple example of processing a file in chunks is below: you
could replace the `process_chunk()` function with any function
that takes a dataframe as input:

```r
library(fst)

df <- data.frame(id = 1:1000,
                 event = sample(c(0, 1), 1000, 
                                replace = TRUE, prob = c(0.88, 0.12)))
# compress = 100 for more compression, slightly slower reads
fst::write_fst(df, "df.fst", compress = 50)

process_chunk <- function(.data) {
    sum(.data$event)
}

# Get info (e.g. number of rows) without reading the
#   full file
file_info <- fst::metadata_fst("df.fst")
total_rows <- file_info$nrOfRows

chunk_starts <- seq(1, total_rows, by = 100)
event_counts <- purrr::map_dbl(chunk_starts, function(start_row) {
    # Don't go past the last row
    end_row <- min(start_row + 99, total_rows)
    chunk <- fst::read_fst("df.fst", from = start_row, to = end_row)
    process_chunk(chunk)
})

event_counts
#>  [1] 16 10  7 12 15 11  9 12 13 18

# Final result: combine the chunk results, e.g. 
#   with bind_rows()
sum(event_counts)
#> [1] 123
```

The package plans to add an `append` option when writing files - once
this becomes available you will also be able to write to a `.fst`
file in chunks.
