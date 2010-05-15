#!/usr/bin/env python
# encoding: utf-8
"""
Show (in MacVim) changes from a specific commit or changes in working
tree relative to the latest commit (sha^..sha or HEAD).

Usage:

    python diff.py [sha]

"""

from subprocess import call
from sys import argv, stderr

from git import Git


__author__ = 'Maciej Konieczny <hello@narf.pl>'


def _main():
    # stop if there's no repo
    Git()

    # show usage info if there are too many arguments
    if len(argv) > 2:
        print >> stderr, __doc__[1:-1]
        exit(1)

    # get sha
    diff_argument = 'HEAD'
    if len(argv) > 1:
        diff_argument ='{sha}^..{sha}'.format(sha=argv[1])

    # do the magic
    call('git diff {0} | mvim -R -'.format(diff_argument), shell=True)

if __name__ == '__main__':
    _main()
