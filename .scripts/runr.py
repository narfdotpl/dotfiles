#!/usr/bin/env python
# encoding: utf-8
"""
Run Ruby any time any tracked file is modified (see: baserun.py).
"""

from baserun import get_files_and_args, run


def main():
    tracked_files, main_file, args = get_files_and_args()
    command = 'ruby %s %s' % (args, main_file)
    run(tracked_files, command)

if __name__ == '__main__':
    main()

