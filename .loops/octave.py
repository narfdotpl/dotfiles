#!/usr/bin/env python
# encoding: utf-8
"""
Run Octave scripts.
"""

from loopozorg import Loop


def _main():
    Loop('octave --silent {main_file} {args}')

if __name__ == '__main__':
    _main()
