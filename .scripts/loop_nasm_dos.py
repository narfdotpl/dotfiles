#!/usr/bin/env python
# encoding: utf-8
"""
Compile and run .asm file any time it's modified. Remove everything but
source afterwards.
"""

from re import sub

from looper import create_if_doesnt_exist, loop, LoopParameters, open_in_editor


def _main():
    lp = LoopParameters()

    if lp.passed_special_parameter:
        create_if_doesnt_exist(lp.main_file)
        open_in_editor(lp.main_file)

    com = sub(r'\.asm$', '.com', lp.main_file)

    command = ';'.join([
        'nasm -o {0} -f bin {1}'.format(com, lp.main_file),
        'dosbox {0} {1}'.format(com, lp.args),
        'rm ' + com
    ])

    loop(lp.tracked_files, command)

if __name__ == '__main__':
    _main()
