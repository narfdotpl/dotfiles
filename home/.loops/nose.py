#!/usr/bin/env python
# encoding: utf-8
"""
Run nosetests.
"""

from loopozorg import Loop


def _main():
    Loop('python `which nosetests` --with-coverage {args}')

if __name__ == '__main__':
    _main()
