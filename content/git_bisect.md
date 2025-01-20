title: Debugging with Git Bisect
author: Hamish Croser
date: 2025-01-20
Category: git
Tags: git,shell,debugging

# Overview

Identifying the specific commit in which a bug was introduced is a great way to start debugging. You can compare the broken commit to the previous commit and identify the change that caused the bug. Sometimes it is clear which commit is the offender, but otherwise it is tedious to go through each commit one by one.

The `git bisect` command facilitates a method to find the first commit in which a bug appeared using a [binary search algorithm](https://en.wikipedia.org/wiki/Binary_search). The method utilises the efficiency of a binary search to cut down the number of tests needed to find the broken commit. If you identify a bug in the latest version, and there are 300 commits between the last known working version and the current version, the Git bisect method will require testing at most 9 versions.

# How to use it

To get started you'll need to know:

- a reliable way to check whether the bug is occurring
- a commit identifier (hash, tag, etc.) of an older commit in which the bug doesn't exist

## Simple approach

1. Check out a commit in which the bug occurs (usually the latest)
2. Enter the following commands to begin:
    ```shell
    $ git bisect start
    $ git bisect bad                 # Current version is bad
    $ git bisect good v1.0.0         # v1.0.0 is known to be good
    ```
3. Git will check out a version between the marked 'good' and 'bad' for testing. Perform the test for the bug.
4. If the version works correctly, enter `git bisect good`. Otherwise, enter `git bisect bad`. If the commit cannot be tested for a reason unrelated to the bug, enter `git bisect skip` and Git will select another commit candidate.
5. Repeat steps 3 and 4 iteratively until the offending commit has been identified.

## Automated approach

The simple approach is useful if your testing must be performed manually. If there is an automated test that will check for the bug, Git bisect can automatically test the versions and return the offending commit. In order to proceed, you will need a script that exits with code 0 if the test has passed and exists with a code between 1 and 127 (inclusive) if the test has failed.

1. Check out a commit in which the bug occurs (usually the latest)
2. Enter the following commands to begin:
    ```shell
    $ git bisect start
    $ git bisect bad                 # Current version is bad
    $ git bisect good v1.0.0         # v1.0.0 is known to be good
    ```
3. Instead of performing the tests yourself, enter `git bisect run <test_script> <arguments>` and Git will use the script to test each version and identify the offending commit once it is complete.

# Git Documentation

There is much more detail about Git bisect in the documentation, which you can find here: <https://git-scm.com/docs/git-bisect>