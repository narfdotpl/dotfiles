#!/usr/bin/env python
# encoding: utf-8
"""
Compile .cs file, run .exe and remove it any time any tracked file is modified.
"""

from re import sub

from looper import create_if_doesnt_exist, loop, LoopParameters, open_in_editor


def _main():
    lp = LoopParameters()

    if lp.passed_special_parameter:
        create_if_doesnt_exist(lp.main_file)
        open_in_editor(lp.main_file)

    exe = sub(r'\.cs$', '.exe', lp.main_file)
    command = 'gmcs {0}; mono {1}; rm {1}'.format(lp.main_file, exe)
    loop(lp.tracked_files, command)

if __name__ == '__main__':
    _main()
