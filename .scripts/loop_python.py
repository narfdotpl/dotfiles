#!/usr/bin/env python
# encoding: utf-8
"""
Run Python and PyFlakes any time any tracked file is modified.
"""

from looper import LoopParameters, loop


def _main():
    lp = LoopParameters()
    command = 'python {0} {1}; pyflakes {2}' \
              .format(lp.args, lp.main_file, ' '.join(lp.tracked_files))
    loop(lp.tracked_files, command)

if __name__ == '__main__':
    _main()
