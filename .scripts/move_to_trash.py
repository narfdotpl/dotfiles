#!/usr/bin/env python
# encoding: utf-8
"""
Move files and directories to Trash (OS X only).

Usage:

    python move_to_trash.py existing_path_1 [existing_path_2 ...]

"""

from itertools import ifilter
from os.path import exists, realpath
from subprocess import call
from sys import argv, stderr


__author__ = 'Maciej Konieczny <hello@narf.pl>'


def move_to_trash(path):
    call("""
        osascript -e '
            tell application "Finder" to delete POSIX file "{0}"
        ' > /dev/null
    """.format(realpath(path)), shell=True)


def usage():
    return __doc__.lstrip('\n').rstrip('\n')


def _main():
    paths = list(ifilter(exists, argv[1:]))
    if not paths:
        print >> stderr, usage()
        exit(1)

    for path in paths:
        move_to_trash(path)

if __name__ == '__main__':
    _main()
