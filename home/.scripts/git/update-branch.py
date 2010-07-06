#!/usr/bin/env python
# encoding: utf-8
"""
Pull (fetch and rebase) master (and rebase current branch against it).

Usage:

    python update-branch.py

"""

from subprocess import call
from sys import argv, stderr

from git import Git


__author__ = 'Maciej Konieczny <hello@narf.pl>'


def system(command):
    return call(command, shell=True)


def _main():
    # stop if there's no repo
    git = Git()

    # show usage info if there are too many arguments
    if len(argv) > 1:
        print >> stderr, __doc__[1:-1]
        exit(1)

    # do the magic
    branch = git.branch
    if branch == 'master':
        system('git pull --rebase')
    else:
        system('git checkout master')
        system('git pull --rebase')
        system('git checkout ' + branch)
        system('git rebase master')


if __name__ == '__main__':
    _main()
