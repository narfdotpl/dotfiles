#!/usr/bin/env python
# encoding: utf-8
"""
Show (in gvim) changes from a specific commit or changes in working
tree relative to the latest commit (`show sha` or `diff HEAD`).

Usage:

    python diff.py [sha]

"""

from subprocess import call
from sys import argv, stderr

from git import Git


__author__ = 'Maciej Konieczny <hello@narf.pl>'


def system(command):
    return call(command, shell=True)


def _main():
    # stop if there's no repo
    Git()

    # show usage info if there are too many arguments
    if len(argv) > 2:
        print >> stderr, __doc__[1:-1]
        exit(1)

    # get sha
    if len(argv) > 1:
        sha = argv[1]
        system('git show {0} | gvim -R -'.format(sha))
    else:
        system('git diff HEAD | gvim -R -')

if __name__ == '__main__':
    _main()
