#!/usr/bin/env python
# encoding: utf-8
"""
Check, compile and run C; remove everything but source.
"""

from loopozorg import Loop


def _main():
    Loop('clang -fsyntax-only {main_file};'
         'splint -realcompare {main_file};'
         'gcc {main_file} -o {bin};'
         './{bin} {args};'
         '[[ -f {bin} ]] && rm {bin}')

if __name__ == '__main__':
    _main()
