#!/usr/bin/env python
# encoding: utf-8
"""
Compile and run .asm file any time it's modified. Remove everything but
source afterwards.
"""

from re import sub

from looper import LoopParameters, loop


def _main():
    lp = LoopParameters()
    output = sub(r'\.asm$', '.o', lp.main_file)
    binary = sub(r'\.asm$', '', lp.main_file)
    command = ';'.join([
        'nasm -f macho -o {0} {1} -DMAC'.format(output, lp.main_file),
        'ld -o {0} {1}'.format(binary, output),
        './' + binary,
        'rm {0} {1}'.format(binary, output)
    ])
    loop(lp.tracked_files, command)

if __name__ == '__main__':
    _main()
