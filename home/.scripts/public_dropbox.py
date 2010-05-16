#!/usr/bin/env python
# encoding: utf-8
"""
Copy/move file to ~/Dropbox/Public and copy public link to clipboard.

Usage:

    python public_dropbox.py copy/move filepath

"""

from os.path import basename, expanduser, isfile, realpath, splitext
from shutil import copy, move
from sys import argv

from utils import exit1, system


__author__ = 'Maciej Konieczny <hello@narf.pl>'


def copy_to_public_dropbox(filepath):
    return _x_to_public_dropbox(copy, filepath)


def move_to_public_dropbox(filepath):
    return _x_to_public_dropbox(move, filepath)


def _x_to_public_dropbox(copy_or_move, filepath):
    # copy/move
    copy_or_move(filepath, expanduser('~/Dropbox/Public'))

    # prepare public link (▲.narf.pl/foo == dl.dropbox.com/u/2618196/foo)
    link = 'http://▲.narf.pl/' + basename(filepath)

    # copy public link to clipboard
    system("echo '{0}' | tr -d '\n' | pbcopy".format(link))

    return link


def _main():
    # read arguments
    try:
        action = argv[1]
        filepath = realpath(expanduser(argv[2]))
    except IndexError:
        exit1(__doc__[1:-1])

    # validate arguments
    if action not in ['copy', 'move']:
        exit1(__doc__[1:-1])
    if not isfile(filepath):
        exit1("'{0}' is not a path to an existing file".format(filepath))

    # do the magic
    if action == 'copy':
        copy_to_public_dropbox(filepath)
    elif action == 'move':
        move_to_public_dropbox(filepath)

if __name__ == '__main__':
    _main()
