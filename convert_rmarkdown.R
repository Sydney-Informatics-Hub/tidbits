#!/usr/bin/env Rscript --vanilla

# compiles all .Rmd files in _R directory into .md files in blog directory,
# if the input file is older than the output file.

# run ./knitpages.R to update all knitr files that need to be updated.
# run this script from your base content directory

library(knitr)

KnitPost <- function(input, outfile, figsfolder, cachefolder, base.url="/") {
  opts_knit$set(base.url = base.url)
  fig.path <- paste0(
    file.path(figsfolder, sub(".Rmd$", "", basename(input))),
    "/"
  )
  print(fig.path)
  cache.path <- file.path(cachefolder, sub(".Rmd$", "", basename(input)))

  opts_chunk$set(fig.path = fig.path)
  opts_chunk$set(cache.path = cache.path)
  render_markdown()
  knit(input, outfile, envir = parent.frame())
}

knit_folder <- function(infolder, outfolder, figsfolder, cachefolder, force = F) {
  for (infile in list.files(infolder, pattern = "*.Rmd", full.names = TRUE)) {

    print(infile)
    outfile = paste0(outfolder, "/", sub(".Rmd$", ".md", basename(infile)))
    print(outfile)

    # knit only if the input file is the last one modified
    if (!file.exists(outfile) | file.info(infile)$mtime > file.info(outfile)$mtime) {
        post_name <- tools::file_path_sans_ext(basename(infile))
        
        KnitPost(infile, outfile, figsfolder, cachefolder, base.url="{attach}")
    }

    # Copy all images in the figure folders to the Pelican
    #   content folder
    local_img_dir <- file.path(infolder, "images")
    global_img_dir <- figsfolder
    img_out_dir <- file.path(outfolder)
    # Don't copy to the full out directory, go one level higher
    file.copy(local_img_dir, img_out_dir,
              recursive = TRUE,
              overwrite = FALSE)
    file.copy(global_img_dir, img_out_dir,
              recursive = TRUE,
              overwrite = FALSE)
  }
}

knit_folder("rmd_content", "content", "images", "cache")