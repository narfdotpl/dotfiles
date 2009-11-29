#!/usr/bin/env python
# encoding: utf-8
"""
Compile and run .asm file any time it's modified. Remove everything but
source afterwards.
"""

from re import sub

from looper import loop, LoopParameters, open_in_editor


def _main():
    lp = LoopParameters()

    if lp.passed_special_parameter:
        open_in_editor(lp.main_file)

    macho = sub(r'\.asm$', '.o', lp.main_file)
    binary = sub(r'\.asm$', '', lp.main_file)
    command = ';'.join([
        'nasm -f macho -o {0} {1} -DMAC'.format(macho, lp.main_file),
        'ld -o {0} {1}'.format(binary, macho),
        './' + binary,
        'rm {0} {1}'.format(binary, macho)
    ])

    loop(lp.tracked_files, command)

if __name__ == '__main__':
    _main()
