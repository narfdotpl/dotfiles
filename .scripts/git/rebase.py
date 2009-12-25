#!/usr/bin/env python
# encoding: utf-8
"""
Run minimal interactive Git rebase.

When working on a non-master branch, rebase `master..branch`.  When working on
master, rebase `origin..HEAD`; if there is no origin, rebase last seven
commits.

If called during a rebase, run `rebase --continue`.
"""

from subprocess import PIPE, Popen, call

from git import Git


__author__ = 'Maciej Konieczny <hello@narf.pl>'


def _main():
    git = Git()

    if git.branch == '(no branch)':
        call('git rebase --continue', shell=True)
    else:
        commit_range = git.minimal_commit_range

        if commit_range:
            count = 0
            for line in Popen(
                ['git', 'shortlog', commit_range, '--summary'],
                stdout=PIPE
            ).stdout:
                count += int(line.split()[0])
        else:
            count = 7

        call('git rebase --interactive HEAD~' + str(count), shell=True)

if __name__ == '__main__':
    _main()
