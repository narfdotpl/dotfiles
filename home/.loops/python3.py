#!/usr/bin/env python
# encoding: utf-8
"""
Run Python 3.
"""

from loopozorg import Loop


def _main():
    Loop('python3 {main_file} {args}')

if __name__ == '__main__':
    _main()
