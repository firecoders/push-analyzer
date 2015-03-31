# Push analyzer

A library for analyzing git pushes. This project is licensed under MIT.

## Why this could be useful

If you want to know what others changed when they pushed (especially when they
altered history), it can get annoying to look at individual commits youself to
figure out which commit was renamed etc. This library can monitor a repository
and output the analysis outcomes.

Also have a look at [gitter][], a bot which broadcasts analysis outcomes to irc
channels.

[gitter]: https://github.com/shak-mar/gitter

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
