# Push analyzer

A script for analyzing git pushes. This project is licensed under MIT.

## Why this is useful to me

I don't quite like the review system github gives you. You pretty much only see
what changes are in a certain branch, but not what changed when someone pushed.
This script analyzes changes to a repository and gives you some nice
information.

## Features

Currently, it can:

* find out whether the push was a force update
* find out whether the push changed the overall diff of the branch or if it just
  cleaned up the history
* detect addition of commits
* detect removal of commits
* detect reordering of commits ( interactive rebase )

The analyze results are stored in dicts, and sent to the formatter via the
observer pattern. The formatter currently just prints out the dicts.

## Plans

This script is designed to collect information which an irc bot could broadcast.
