#!/usr/bin/env python
# encoding: utf-8
"""
Run Ruby with warnings turned on.

If called without arguments, run Interactive Ruby with simple prompt.
"""

from subprocess import call
from sys import argv


def _main():
    args = ' '.join(argv[1:])
    if args:
        command = 'ruby -w ' + args
    else:
        command = 'irb --simple-prompt'
    call(command, shell=True)

if __name__ == '__main__':
    _main()
