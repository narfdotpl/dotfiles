#!/usr/bin/env python
# encoding: utf-8
"""
Run Ruby any time any tracked file is modified.
"""

from looper import create_if_doesnt_exist, loop, LoopParameters, open_in_editor


def _main():
    lp = LoopParameters()

    if lp.passed_special_parameter:
        create_if_doesnt_exist(lp.main_file)
        open_in_editor(lp.main_file)

    command = 'ruby {0} {1}'.format(lp.args, lp.main_file)
    loop(lp.tracked_files, command)

if __name__ == '__main__':
    _main()
