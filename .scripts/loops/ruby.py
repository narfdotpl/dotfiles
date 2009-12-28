#!/usr/bin/env python
# encoding: utf-8
"""
Run Ruby.
"""

from loop import Loop


def _main():
    Loop('ruby {main_file} {args}')

if __name__ == '__main__':
    _main()
