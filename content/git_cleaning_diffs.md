Title: Cleaning a git diff
Date: 2020-07-02
Category: git
Tags: git,shell,github,code review

Code review is easiest when the changes offered by a *head branch* onto a *base
branch* are focussed on a single purpose of change.  When they are not, the
diff shown in GitHub can be long and hard to read, and the pull request is more
susceptible to merge conflicts.

Here we use "diff" (elsewhere "patch") to refer to what's seen on the Files
Changed tab in GitHub.

This tidbit proposes to give some hints about how you can use git to isolate
the changes relevant to a specific pull request, i.e. to "clean the diff",
using git shell commands.

## Case study

We have been supporting the maintainers of the Hydromad R package to adopt
contemporary best practices around open-source software maintenance.

Pull Request [#112](https://github.com/josephguillaume/hydromad/pull/112)
proposed to resolve
[#61](https://github.com/josephguillaume/hydromad/issues/61$): making the
pacakge conform with the CRAN requirement that package code does not use
`library` or `require`.

Two things made this contribution difficult to process:

1. The contributor made changes beyond the scope of the PR, additionally
   resolving linter complaints of long lines, etc, by reformatting those lines.
2. A new commit had been added to master in the meantime, performing wholesale
   stylistic changes across the codebase, but not identical to the changes made
   by the contributor.

This post covers some of the questions and ideas raised there.
"Splitting one branch into multiple patches" below is the main solution.

## Preface: What does the diff in GitHub show?

The diff in GitHub compares each file in the HEAD commit of the head branch to
each file in the base branch... But not always the latest ("HEAD") commit of
the base branch.

GitHub will firstly try to merge the latest base branch into the head branch.
This will be successful if one of the following conditions can be met:
* There are no new commits on the base branch (i.e. the head is built by
  appending commits to the latest base commit). This is called a "fast forward
  merge".
* Any new commits on the base branch modify only different files, or different
  parts of the same file, such that Git can perform an "automatic merge". Note
  that an automatic merge *can* be incorrect, which is one reason that
  automated testing (e.g. with GitHub workflows) is invaluable.

If successful, GitHub's diff **will compare the head branch to the base
branch** through the merge commit, thus showing only those changes introduced
in the head branch.

If unsuccessful, GitHub's diff **will compare the head branch to the **nearest
common ancestor commit** shared by the head branch and the base branch.  This
might be the point in the base branch that the contributor started building on,
or it might be the latest time the contributor merged in commits from the base
branch.

## Preface: Starting from the right point

Prevention first! *Before you make any changes*, you can reduce the chance of
merge conflicts by making sure you're building on the latest version of the
base branch. Assuming the base branch is on the remote called `origin` in the
branch called `master`, the following will create a new branch in your working
copy based on the latest master, and check it out (i.e. get in to the branch to
work on it):

```sh
git fetch origin
git checkout -b my-new-branch origin/master
```

### Aside: working with a fork

If you're developing a pull request from a fork of some central repo, you might
want to branch from that "upstream" master instead. Do so by adding the
upstream as a remote:

```sh
git add origin https://github.com/my-username/some-repo
git add upstream https://github.com/central-username/some-repo
git fetch upstream
git checkout -b my-new-branch upstream/master  # like above
git push -u origin my-new-branch
```

This branches from `upstream`, but pushes to `origin`.

## Preface: Making a backup of your work

If you've already made changes, you shouldn't have to worry about losing your
current work before trying risky Git operations. Some people use `git stash`
for this, but I recommend just creating a commit.

Commit all changes (NB: staged and unstaged changes included):
```sh
git status                  # Check for any files you've forgotten to add
git add path/to/new/files   # Add any files you've forgotten to add
git commit -a -m WIP        # Commit all changes, but leave a message for
                            # myself that this commit is a work-in-progress
```

The name (SHA ref) of the new commit should be shown after committing, or you
can get it from `git log`. Note it somewhere if you might want to refer to it
later.
Or, give a name to your latest commit by copying it into another branch:
```sh
git branch -b new-backup-branch-name
```

Once you've safely made a backup, you can undo your commit and keep working on
your changes:

```sh
git reset HEAD^             # Undo the commit, but leave the files changed
```

Note that this doesn't *delete* the commit, it just removes it from your
current branch.  You can still reference the old commit using that SHA ref
you noted down, or the name of that backup branch.

## Should I worry about cleaning up the list of commits?

Below we talk about cleaning up the diff: the set of changes to files.
You might also want a neat commit history, but IMO it's not usually worth
neatening up the commit history shown in a pull request.

Why? One neat feature of GitHub is the option to "Squash and Merge" a pull
request onto the base branch when it is merged. This means that all of the mess
of commits made along the way will be turned into a single commit.

This means that you can focus on the diff and make as many messy commits as you
like to get to the right place.

## Not committing all your changes

If you've made changes in your working copy, some of which you want to commit
because they're related to the pull request you are building, and some of which
you don't want to commit (because they're only for your local use, or because
you want to stash them for a different pull request), there are several useful
tools. Most important, perhaps, is `git add --patch` (or `git add -p`).

First, some tools to check what would be committed if you did `git commit` at
any point:
```sh
git status         # show an overview of what's staged to be committed and what's not
git diff --cached  # show lines you've already staged to be committed
git diff           # show lines you've not already staged to committed
```

To add only selected parts of files, use:
```sh
git add --patch           # select all the lines to add
git commit                # when you're ready...
```
This is an interactive process, in which you type `y` for chunks you want to
keep, and `n` for chunks you don't. Try it! Press `?` for other commands.

If you have a new file in your repo directory that's not known to git, the
following tells git about that path (adds it to the index) without staging its
lines:

```sh
git add -N path/to/file   # repeat for each new file
git add --patch           # select which lines to add, from all your uncommited files
git commit                # when you're ready...
```

Removing files from the commit: If you've staged something and decide you don't
want to commit that (whole) file:

```sh
git reset path/to/file
```

## Undoing a commit but keeping the changes

This will undo the latest commit, but keep the changes to the files in your
working copy, allowing you to do a patch commit or similar.

```sh
git reset HEAD^
```
Again, you can follow this with `git add --patch` and `git commit`.

## Selecting only some commits

Sometimes there are good things localised in past commits... or bad things you
want to remove from a diff.

NB: You might want to make a backup of your work first.

You can show what was in a specific commit with:
```sh
git show some-commit-ref
```

If you want to select only some commits, you have a few options:

* interactive rebase: this is really powerful, but may take a bit of practice
  to get used to. Identify a good commit you've built on, then use `git rebase
  -i that-good-commit-ref`, and edit the file shown to pick or skip commits
  since then that you want. You will need to force-push any changes to GitHub
  `git push -f`.
* adopt only selected commits with `cherry-pick`: Start a clean branch `git
  checkout -b new-branch-name that-good-commit-ref` and use `git cherry-pick`
  to adopt individual commits from your changes. Make sure to do it in order.
* undo selected commits with `git revert`.

## Undoing changes to some files

Often you're happy with the diff you've got on some files, but not with others.
You can use `git checkout` to adopt the state of a selected file from a
selected commit/branch.

NB: You might want to make a backup of your work first.

Let's say you've changed some file called `path/to/file` and committed those
changes, but now want to adopt whatever is in the base branch (because the
change was irrelevant to the current pull request, or because there were
conflicting changes in the base which you prefer).
Let's assume the base branch is called `master` on a remote called `origin`.

Then you can adopt the version from `origin/master` with:

```sh
git fetch origin      # Make sure we have the latest origin/master branch
git checkout origin/master path/to/file
```

If you want to try before you buy, you can *look* at the version from
origin/master with:
```sh
git show origin/master:path/to/file
```
or save it to some other path with:
```sh
git show origin/master:path/to/file > /tmp/put-it-here-please
```

## Splitting one branch into multiple patches

Back to the case study: In a complicated situation like this, we may have a
long history of commits composing the current messy diff.  One approach to
resolving this is to create several separate branches (and corresponding pull
requests) with more focussed diffs.

1. Create a copy of the current branch where we will commit the first patch
   `git checkout -b patch1`.
2. Find a common place to start, the nearest common ancestor with origin's
   master: `base=$(git merge-base HEAD origin/master)`. Here we are using
   a bash feature to store the merge base ref in a variable called `$base`.
   View it with `echo $base`.
3. Reset `patch1` back to `$base`, keeping all changes, but not adding them.
   `git reset $base`.
4. Add parts of files that you want `git add --patch`.
5. Add any whole files that are missing from the patch with `git status` then
   `git add path/to/file`.
6. Commit `git commit -m "blah blah blah"`, then push this branch if
   appropriate.
7. If you look at `git diff`, the remainder should be changes you want in
   another patch commit. Let's open a new branch like `patch2` at `$base`
   keeping those changes in our working copy: `git checkout -b patch2 $base`.
8. Repeat from step 4. until all the changes have been committed (and pushed,
   and pull requests opened) in a focussed pull request.
