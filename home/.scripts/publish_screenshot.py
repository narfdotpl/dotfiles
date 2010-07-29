#!/usr/bin/env python
# encoding: utf-8
"""
Rename latest screenshot, reduce its size, upload it to Dropbox, and
copy public link to clipboard.

Usage:

    python publish_screenshot.py [<new name>]

"""

from datetime import datetime as dt
from os import listdir
from os.path import basename, dirname, expanduser, join, realpath, splitext
from shutil import move
from sys import argv

from utils import exit1, move_to_public_dropbox, system


__author__ = 'Maciej Konieczny <hello@narf.pl>'


def get_latest_screenshot(directory='~/Desktop'):
    screenshots = []
    directory = realpath(expanduser(directory))

    for filename in listdir(directory):
        if filename.startswith('Screen shot ') and filename.endswith('.png'):
            screenshots.append(filename)

    if screenshots:
        return join(directory, sorted(screenshots)[-1])


def rename(full_path, new_name):
    directory = dirname(full_path)
    name, extension = splitext(basename(full_path))
    new_full_path = join(directory, new_name + extension)
    move(full_path, new_full_path)
    return new_full_path


def _main():
    # get new name or use current datetime
    new_name = '-'.join(argv[1:]) or dt.strftime(dt.now(), '%y%m%d-%H%M%S')

    # get latest screenshot
    screenshot = get_latest_screenshot()
    if not screenshot:
        exit1('No screenshots found.')

    # rename it
    screenshot = rename(screenshot, new_name)

    # reduce its size
    system("optipng -quiet '{0}'".format(screenshot))

    # upload to dropbox and copy public link (and print it)
    print move_to_public_dropbox(screenshot)

if __name__ == '__main__':
    _main()
