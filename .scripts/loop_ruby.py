#!/usr/bin/env python
# encoding: utf-8
"""
Run Ruby any time any tracked file is modified.
"""

from baseloop import get_files_and_args, loop


def _main():
    tracked_files, main_file, args = get_files_and_args()
    command = 'ruby {0} {1}'.format(args, main_file)
    loop(tracked_files, command)

if __name__ == '__main__':
    _main()

