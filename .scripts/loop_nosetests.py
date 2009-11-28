#!/usr/bin/env python
# encoding: utf-8
"""
Run nosetests and PyFlakes any time any tracked file is modified.
"""

from looper import LoopParameters, loop


def _main():
    lp = LoopParameters()
    command = 'nosetests --with-coverage {0}; pyflakes {1}' \
              .format(lp.args, ' '.join(lp.tracked_files))
    loop(lp.tracked_files, command)

if __name__ == '__main__':
    _main()
