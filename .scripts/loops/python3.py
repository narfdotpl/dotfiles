#!/usr/bin/env python
# encoding: utf-8
"""
Run Python 3 any time any tracked file is modified.
"""

from looper import create_if_doesnt_exist, loop, LoopParameters, open_in_editor


def _main():
    lp = LoopParameters()

    if lp.passed_special_parameter:
        create_if_doesnt_exist(lp.main_file, 'python3')
        open_in_editor(lp.main_file)

    command = 'python3 {0} {1}'.format(lp.main_file, lp.args)
    loop(lp.tracked_files, command)

if __name__ == '__main__':
    _main()
