#!/usr/bin/env python
# encoding: utf-8
"""
Base script for automatically running commands on file modification.

example:

    $ alias loop="python sth_that_imports_looper.py"  # see: loop_python.py

    $ loop myfile
    => tracked_files = ['myfile']
       main_file = 'myfile'
       args = ''

    $ loop `find . -name "*.py"` foo.py -my args
    => tracked_files = ['./foo.py', './bar.py', 'foo.py']
       main_file = 'foo.py'
       args = '-my args'

"""

import os
import stat
from sys import argv
from time import sleep


__author__ = 'Maciej Konieczny <hello@narf.pl>'


class LoopParameters(object):
    """
    Attributes: args, main_file, tracked_files.
    """

    def __init__(self):
        # get args
        for i, word in enumerate(argv):
            if word.startswith('-'):
                self.args = ' '.join(argv[i:])
                break
        else:  # if no break
            self.args = ''
            i += 1

        # get tracked files and main file paths
        self.tracked_files = argv[1:i]
        self.main_file = self.tracked_files[-1]


def loop(tracked_files, command):
    """
    Check every second whether any of the tracked files has been modified.
    If it has, clear the screen and run `command`.
    """

    mtime = lambda filepath: os.stat(filepath)[stat.ST_MTIME]
    old_mtime_sum = -1

    while True:
        new_mtime_sum = sum(mtime(f) for f in tracked_files)  # <3 py3 map()
        if old_mtime_sum != new_mtime_sum:
            old_mtime_sum = new_mtime_sum
            os.system('clear;' + command)
        sleep(1)  # one second
