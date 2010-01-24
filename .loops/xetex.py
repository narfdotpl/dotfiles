#!/usr/bin/env python
# encoding: utf-8
"""
Compile XeTeX file and remove everything but source and the pdf.
"""

from loopozorg import Loop


def _main():
    loop = Loop()
    loop.aux = loop.bin + '.aux'
    loop.log = loop.bin + '.log'
    loop.run('xelatex {main_file};'
             '[[ -f {aux} ]] && rm {aux};'
             '[[ -f {log} ]] && rm {log}')

if __name__ == '__main__':
    _main()
