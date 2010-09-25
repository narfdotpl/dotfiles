#!/usr/bin/env python
# encoding: utf-8
"""
Run Python.
"""

from loopozorg import Loop


def _main():
    loop = Loop()
    loop.run('python {main_file} {args}',
             template='~/.loops/templates/python.txt')

if __name__ == '__main__':
    _main()
