#!/usr/bin/env python
# encoding: utf-8
"""
Replace $HOME with ~ and limit path to three trailing components.

Usage:

    python short_path.py <path>

"""

from os.path import expanduser
from sys import argv

from utils import exit1


__author__ = 'Maciej Konieczny <hello@narf.pl>'


def short_path(path, limit=3):
    # replace $HOME with ~
    home = expanduser('~')
    if path.startswith(home):
        path = path.replace(home, '~', 1)

    # limit path to given number of trailing components
    if limit:
        components = path.split('/')
        how_many = len(components)
        if components[0] == '':
            how_many -= 1

        if how_many > limit:
            path = '/'.join(components[-limit:])

    return path


def _main():
    # show usage info if there is different number of arguments than one
    if len(argv) != 2:
        exit1(__doc__[1:-1])

    # do the magic
    path = argv[1]
    print short_path(path)

if __name__ == '__main__':
    _main()
