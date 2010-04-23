#!/usr/bin/env python
# encoding: utf-8
"""
Compile and run C#; remove everything but source.
"""

from loopozorg import Loop


def _main():
    loop = Loop()
    loop.exe = loop.bin + '.exe'
    loop.run('gmcs {main_file} && mono {exe} {args};'
             '[[ -f {exe} ]] && rm {exe}')

if __name__ == '__main__':
    _main()
