#!/usr/bin/env python
# encoding: utf-8
"""
Create root branch.

Usage:

    python root-branch.py <name>

"""

from subprocess import call
from sys import argv, stderr

from git import Git


__author__ = 'Maciej Konieczny <hello@narf.pl>'


def exit1(message):
    print >> stderr, message
    exit(1)


def safe(command):
    if command:
        return_code = call(command, shell=True)
        if return_code != 0:
            raise EnvironmentError(return_code, 'Something went wrong with '
                                              '"{0}" command.'.format(command))


def _main():
    # stop if there's no repo
    git = Git()

    # ensure working directory is clean
    if not git.is_clean:
        exit1('Working directory is not clean. Commit, stash or remove your '
              'changes and try again.')

    # get new branch name
    if len(argv) != 2:
        exit1(__doc__[1:-1])
    branch = argv[1]

    # check if branch exists
    if branch in git.branches:
        exit1('Branch "{0}" already exists.'.format(branch))

    # go to toplevel dir (this doesn't work if the script is used as a git
    # alias, because git invokes them from toplevel dir)
    safe('cd ..;' * git.depth)

    # create new ref
    safe('git symbolic-ref HEAD refs/heads/' + branch)

    # clear index
    safe('rm .git/index')
    safe('git clean --force -d -x')

    # create (empty) informational commit
    safe('git commit --allow-empty --message "created root branch {0}"'
         .format(branch))

if __name__ == '__main__':
    _main()
