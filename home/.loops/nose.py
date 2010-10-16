#!/usr/bin/env python
# encoding: utf-8
"""
Run nosetests.
"""

from loopozorg import Loop


def _main():
    Loop('rm `find . -name "*.pyc"` 2> /dev/null;'
         'python `which nosetests` --with-coverage {args}')

if __name__ == '__main__':
    _main()
