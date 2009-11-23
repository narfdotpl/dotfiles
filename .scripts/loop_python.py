#!/usr/bin/env python
# encoding: utf-8
"""
Run Python and PyFlakes any time any tracked file is modified.
"""

from baseloop import get_files_and_args, loop


def _main():
    tracked_files, main_file, args = get_files_and_args()
    command = 'python {0} {1}; pyflakes {2}' \
              .format(args, main_file, ' '.join(tracked_files))
    loop(tracked_files, command)

if __name__ == '__main__':
    _main()

