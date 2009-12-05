#!/usr/bin/env python
# encoding: utf-8
"""
Run Fabric with given arguments and check `fabfile.py` with PyFlakes any
time it is modified.
"""

from looper import create_if_doesnt_exist, loop, LoopParameters, open_in_editor


def _main():
    lp = LoopParameters()

    # dirty hack
    args = ' '.join(lp.tracked_files)
    lp.main_file = 'fabfile.py'
    lp.tracked_files = [lp.main_file]

    if lp.passed_special_parameter:
        create_if_doesnt_exist(lp.main_file, 'python')
        open_in_editor(lp.main_file)

    command = 'fab {0}; pyflakes fabfile.py'.format(args)
    loop(lp.tracked_files, command)

if __name__ == '__main__':
    _main()
