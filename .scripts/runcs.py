#!/usr/bin/env python
# encoding: utf-8
"""
Compile .cs file, run .exe and remove it any time any tracked file is
modified (see: baserun.py).
"""

import re

from baserun import get_files_and_args, run


def main():
    tracked_files, main_file, args = get_files_and_args()
    exe_file = re.sub(r'\.cs$', '.exe', main_file)
    command = 'gmcs %s; mono %s; rm %s' % (main_file, exe_file, exe_file)
    run(tracked_files, command)

if __name__ == '__main__':
    main()

