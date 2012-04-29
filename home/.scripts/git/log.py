#!/usr/bin/env python
# encoding: utf-8
"""
Show minimal Git log.

Usage:

    python log.py

When working on a non-master branch, show `master..branch` log.  When
working on master, show `origin..HEAD` log; if there is no origin, show
last seven commits.

Formatting example:

    2009-12-12 simplified references to websites
    2009-12-18 moved editor settings to one place

"""

from subprocess import call
from sys import argv, stderr

from git import Git


__author__ = 'Maciej Konieczny <hello@narf.pl>'


def _main():
    # show usage info if there any arguments
    if len(argv) > 1:
        print >> stderr, __doc__[1:-1]
        exit(1)

    # stop if there's no repo
    git = Git()

    # do the magic
    command = ' '.join([
        'git log',
        git.minimal_commit_range or '--max-count=7',
        '--reverse --pretty=format:"%ad %s" --date=short'
    ])
    call(command, shell=True)
    print

if __name__ == '__main__':
    _main()
