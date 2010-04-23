#!/usr/bin/env python
# encoding: utf-8
"""
Run minimal interactive Git rebase.

When working on a non-master branch, rebase `master..branch`.  When
working on master, rebase `origin..HEAD`; if there is no origin, rebase
last seven commits.

If called during a rebase, run `rebase --continue`.  If called with
arguments, act as an alias.
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
            commit_range = git.minimal_commit_range or ''

            # get number of commits
            number_of_commits = 0
            for line in Popen(
                'git shortlog {0} --summary'.format(commit_range),
                shell=True, stdout=PIPE
            ).stdout:
                number_of_commits += int(line.split()[0])

            # if there is no origin, rebase last seven commits
            if not commit_range:
                number_of_commits -= 1  # can't rebase initial commit
                max_number = 7
                if number_of_commits > max_number:
                    number_of_commits = max_number

            command += '--interactive HEAD~' + str(number_of_commits)

    call(command, shell=True)

if __name__ == '__main__':
    _main()
