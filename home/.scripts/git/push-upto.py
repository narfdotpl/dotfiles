#!/usr/bin/env python
# encoding: utf-8
"""
Push changes to origin up to specific commit.

Usage:

    python push-upto.py <sha> [<push options>]

"""

from subprocess import call
from sys import argv, stderr

from git import Git


__author__ = 'Maciej Konieczny <hello@narf.pl>'


def _main():
    # stop if there's no repo
    git = Git()

    # show usage info if there are not enough arguments
    if len(argv) < 2:
        print >> stderr, __doc__[1:-1]
        exit(1)

    # do the magic
    call('git push {options} origin {sha}:{branch}'.format(
        sha=argv[1],
        options=' '.join(argv[2:]),
        branch=git.branch
    ), shell=True)

if __name__ == '__main__':
    _main()
