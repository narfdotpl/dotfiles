#!/usr/bin/env python
# encoding: utf-8
"""
Run Python with warnings about nontrivial Python 3 incompatibilities and
check all files with PyFlakes.
"""

from loop import Loop


def _main():
    Loop('python -3 {main_file} {args};'
         'pyflakes {tracked_files}')

if __name__ == '__main__':
    _main()
