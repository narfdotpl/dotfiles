#!/usr/bin/env python
# encoding: utf-8
"""
Run Ruby any time any tracked file is modified.
"""

from baseloop import get_files_and_args, loop


def main():
    tracked_files, main_file, args = get_files_and_args()
    command = 'ruby %s %s' % (args, main_file)
    loop(tracked_files, command)

if __name__ == '__main__':
    main()

