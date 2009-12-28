#!/usr/bin/env python
# encoding: utf-8
"""
Compile assembly and run it in DOSBox; remove everything but source.
"""

from loopozorg import Loop


def _main():
    loop = Loop()
    loop.com = loop.bin + '.com'
    loop.run('nasm -o {com} -f bin {main_file};'
             'dosbox {com} {args};'
             'rm {com}')

if __name__ == '__main__':
    _main()