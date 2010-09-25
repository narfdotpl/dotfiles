#!/usr/bin/env python
# encoding: utf-8
"""
Run Python with warnings about nontrivial Python 3 incompatibilities.
"""

from loopozorg import Loop


def _main():
    Loop('python -3 {main_file} {args}')

if __name__ == '__main__':
    _main()
