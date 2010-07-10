#!/usr/bin/env python
# encoding: utf-8
"""
Push current branch to "backup" remote.

Usage:

    python backup.py [push options]

"""

from pipes import quote
from subprocess import call
from sys import argv

from git import Git


__author__ = 'Maciej Konieczny <hello@narf.pl>'


def _main():
    # stop if there's no repo
    git = Git()

    # read options
    options = ' '.join(map(quote, argv[1:]))

    # do the magic
    return call('git push {0} backup {1}'.format(options, git.branch),
                shell=True)

if __name__ == '__main__':
    _main()
