#!/usr/bin/env python
# encoding: utf-8
"""
Compile XeTeX.
"""

from loopozorg import Loop


def _main():
    Loop('xelatex {main_file}')

if __name__ == '__main__':
    _main()
