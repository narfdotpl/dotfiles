#!/usr/bin/env python
# encoding: utf-8
"""
Compile and run .asm file any time it's modified. Remove everything but
source afterwards.
"""

from re import sub

from baseloop import get_files_and_args, loop


def _main():
    tracked_files, main_file, args = get_files_and_args()
    output = sub(r'\.asm$', '.o', main_file)
    binary = sub(r'\.asm$', '', main_file)
    command = ';'.join([
        'nasm -f macho -o {0} {1} -DMAC'.format(output, main_file),
        'ld -o {0} {1}'.format(binary, output),
        './' + binary,
        'rm {0} {1}'.format(binary, output)
    ])
    loop(tracked_files, command)

if __name__ == '__main__':
    _main()
