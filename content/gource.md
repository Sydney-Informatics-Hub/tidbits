title: Show off your development history with gource
author: Marius Mather
date: 2021-07-23
Category: git
Tags: git,shell,fun

Want to show off your hard work on a project? [gource](https://gource.io/)
displays the history of a git repo with a cool moving
visualisation of how the files + folders have been worked on over time.
You can install it through homebrew: `brew install gource`.

Here's the 10 year history of the OMIA project as a 1 minute video:

<video controls width="600" preload="metadata">
<source src="{attach}downloads/omia_gource.m4v" type="video/mp4">
</video>

By default, running `gource` in a directory with a git repo
will generate a moving visualisation of the commit history -
depending on the speed of development on your project there
are a lot of settings you can tweak to get better results.
For `omia` I ended up with:

```shell
gource --filename-time 10.0 --date-format "%B %Y" --hide filenames --time-scale 4.0 --seconds-per-day 0.2 --auto-skip-seconds 0.1
```

Also check the project's [documentation](https://github.com/acaudwell/Gource/wiki/Videos)
for how to export this to a video file using tools like `ffmpeg`.