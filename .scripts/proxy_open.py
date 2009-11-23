#!/usr/bin/env python
# encoding: utf-8
"""
Proxy `open` command; if used without arguments, open working directory
in finder.
"""

from os import system
from sys import argv


def _main():
    args = ' '.join(argv[1:])
    if args:
        system('open ' + args)
    else:
        system('open `pwd`')

if __name__ == '__main__':
    _main()

