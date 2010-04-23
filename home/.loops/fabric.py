#!/usr/bin/env python
# encoding: utf-8
"""
Run Fabric with given arguments and check `fabfile.py` with PyFlakes.
"""

from loopozorg import Loop


def _main():
    loop = Loop()
    loop.tracked_files = ['fabfile.py']
    loop.run('fab {raw};'
             'pyflakes {main_file}')

if __name__ == '__main__':
    _main()
