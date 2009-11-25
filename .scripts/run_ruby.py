#!/usr/bin/env python
# encoding: utf-8
"""
Run Ruby with warnings turned on.

If used without arguments, run Interactive Ruby with simple prompt.
"""

from os import system
from sys import argv


def _main():
    args = ' '.join(argv[1:])
    if args:
        system('ruby -w ' + args)
    else:
        system('irb --simple-prompt')

if __name__ == '__main__':
    _main()
