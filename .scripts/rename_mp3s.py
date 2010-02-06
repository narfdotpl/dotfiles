#!/usr/bin/env python
# encoding: utf-8
"""
Rename all *.mp3 files in the current directory like this:

    '03 Eunuch Provocateur.mp3' -> '03-eunuch_provocateur.mp3'

"""

from os import listdir, rename
from os.path import isfile


def _main():
    for name in listdir('.'):
        if name.endswith('.mp3') and isfile(name):
            new_name = name.lower().replace(' ', '-', 1).replace(' ', '_')
            rename(name, new_name)

if __name__ == '__main__':
    _main()
