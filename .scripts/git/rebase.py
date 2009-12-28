#!/usr/bin/env python
# encoding: utf-8
"""
Run minimal interactive Git rebase.

When working on a non-master branch, rebase `master..branch`.  When working on
master, rebase `origin..HEAD`; if there is no origin, rebase last seven
commits.

If called during a rebase, run `rebase --continue`.  If called with arguments,
act as an alias.
"""

from subprocess import PIPE, Popen, call
from sys import argv

from git import Git


__author__ = 'Maciej Konieczny <hello@narf.pl>'


def _main():
    git = Git()

    command = 'git rebase '
    args = ' '.join(argv[1:])

    if args:
        command += args
    else:
        if git.branch == '(no branch)':
            command += '--continue'
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

            command += '--interactive HEAD~' + str(count)

    call(command, shell=True)

if __name__ == '__main__':
    _main()
