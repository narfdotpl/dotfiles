#!/usr/bin/env python
# encoding: utf-8
"""
Compile .cs file, run .exe and remove it any time any tracked file
is modified.
"""

from re import sub

from baseloop import get_files_and_args, loop


def _main():
    tracked_files, main_file, args = get_files_and_args()
    exe_file = sub(r'\.cs$', '.exe', main_file)
    command = 'gmcs {0}; mono {1}; rm {1}'.format(main_file, exe_file)
    loop(tracked_files, command)

if __name__ == '__main__':
    _main()
