#!/usr/bin/env python
# encoding: utf-8
"""
Compile assembly and run it in DOSBox; remove everything but source.
"""

from os.path import splitext

from loopozorg import Loop


def _main():
    loop = Loop()
    loop.com = splitext(loop.main_file)[0] + '.com'
    loop.run('nasm -o {com} -f bin {main_file};'
             'dosbox {com} {args};'
             'rm {com}')

if __name__ == '__main__':
    _main()
