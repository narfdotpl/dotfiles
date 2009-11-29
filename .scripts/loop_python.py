#!/usr/bin/env python
# encoding: utf-8
"""
Run Python and PyFlakes any time any tracked file is modified.
"""

from looper import create_if_doesnt_exist, loop, LoopParameters, open_in_editor


def _main():
    lp = LoopParameters()

    if lp.passed_special_parameter:
        create_if_doesnt_exist(lp.main_file)
        open_in_editor(lp.main_file)

    command = 'python {0} {1}; pyflakes {2}' \
              .format(lp.args, lp.main_file, ' '.join(lp.tracked_files))
    loop(lp.tracked_files, command)

if __name__ == '__main__':
    _main()
