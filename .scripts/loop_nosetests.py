#!/usr/bin/env python
# encoding: utf-8
"""
Run nosetests and PyFlakes any time any tracked file is modified.
"""

from baseloop import get_files_and_args, loop


def main():
    tracked_files, main_file, args = get_files_and_args()
    command = 'nosetests --with-coverage %s; pyflakes %s' \
              % (args, ' '.join(tracked_files))
    loop(tracked_files, command)

if __name__ == '__main__':
    main()

