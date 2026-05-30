# Contributing to Presentation Control Tool

First off, thank you for considering contributing to the Presentation Control Tool! It's people like you that make this tool better for everyone.

## Where do I go from here?

If you've noticed a bug or have a feature request, make sure to open an issue if one doesn't already exist. If you'd like to work on a feature, you can open an issue first to discuss it or just open a pull request directly!

## Fork & create a branch

If this is something you think you can fix, then fork the repository and create a branch with a descriptive name.

A good branch name would be (where issue #325 is the ticket you're working on):

```sh
git checkout -b 325-add-new-gesture
```

## Get the test suite running

Make sure your changes don't break the existing code by running the test suite:

```bash
python -m unittest discover tests
```

## Implement your fix or feature

At this point, you're ready to make your changes! Feel free to ask for help if you need it.

## Make a Pull Request

At this point, you should switch back to your master branch and make sure it's up to date with the original repository's master branch:

```sh
git remote add upstream https://github.com/rab781/Presentation-Tools.git
git checkout master
git pull upstream master
```

Then update your feature branch from your local copy of master, and push it!

```sh
git checkout 325-add-new-gesture
git rebase master
git push --set-upstream origin 325-add-new-gesture
```

Finally, go to GitHub and make a Pull Request!
