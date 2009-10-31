#!/usr/bin/env python
# encoding: utf-8
"""
Compile .cs file, run .exe and remove it any time any tracked file
is modified.
"""

import re

from baseloop import get_files_and_args, loop


def main():
    tracked_files, main_file, args = get_files_and_args()
    exe_file = re.sub(r'\.cs$', '.exe', main_file)
    command = 'gmcs %s; mono %s; rm %s' % (main_file, exe_file, exe_file)
    loop(tracked_files, command)

if __name__ == '__main__':
    main()

