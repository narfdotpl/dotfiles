#!/usr/bin/env python
# encoding: utf-8
"""
Rename all *.jpg files in the current directory like this:

    '2010-01-07 16.18.30.jpg' -> '100107_1618_30.jpg'

"""

from datetime import datetime
from os import listdir, rename
from os.path import isfile


__author__ = 'Maciej Konieczny <hello@narf.pl>'


def _main():
    extension = '.jpg'
    old_format = '%Y-%m-%d %H.%M.%S' + extension
    new_format = '%y%m%d_%H%M_%S' + extension

    for name in listdir('.'):
        if name.endswith(extension) and isfile(name):
            try:
                time = datetime.strptime(name, old_format)
            except ValueError:  # except file name doesn't match the pattern
                pass
            else:
                new_name = time.strftime(new_format)
                rename(name, new_name)
                print '{0}  ->  {1}'.format(name, new_name)

if __name__ == '__main__':
    _main()
