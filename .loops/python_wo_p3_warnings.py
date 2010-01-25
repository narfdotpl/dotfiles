#!/usr/bin/env python
# encoding: utf-8
"""
Run Python and check all files with PyFlakes.
"""

from loopozorg import Loop


def _main():
    loop = Loop()
    loop.run('python {main_file} {args};'
             'pyflakes {tracked_files}',
             template='~/.loops/templates/python.txt')

if __name__ == '__main__':
    _main()
