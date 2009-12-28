#!/usr/bin/env python
# encoding: utf-8
"""
Run nosetests and check all files with PyFlakes.
"""

from loop import Loop


def _main():
    Loop('python `which nosetests` --with-coverage {args};'
         'pyflakes {tracked_files}')

if __name__ == '__main__':
    _main()
