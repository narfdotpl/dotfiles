#!/usr/bin/env python
# encoding: utf-8
"""
Run Python 3 any time any tracked file is modified.
"""

from looper import LoopParameters, loop


def _main():
    lp = LoopParameters()
    command = 'python3 {0} {1}'.format(lp.args, lp.main_file)
    loop(lp.tracked_files, command)

if __name__ == '__main__':
    _main()
