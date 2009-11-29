#!/usr/bin/env python
# encoding: utf-8
"""
Base script for automatically running commands on file modification.

No pretty errors for executing it with not enough parameters.

example:

    $ alias loop="python sth_that_imports_looper.py"  # see: loop_python.py

    $ loop myfile
    => tracked_files = ['myfile']
       main_file = 'myfile'
       args = ''
       passed_special_parameter = False

    $ loop + myfile
    => tracked_files = ['myfile']
       main_file = 'myfile'
       args = ''
       passed_special_parameter = True

    $ loop `find . -name "*.py"` foo.py -my args
    => tracked_files = ['./foo.py', './bar.py', 'foo.py']
       main_file = 'foo.py'
       args = '-my args'
       passed_special_parameter = False

"""

import os
from os import system
from os.path import dirname, exists, join, realpath
import stat
import sys
from time import sleep


__author__ = 'Maciej Konieczny <hello@narf.pl>'


class LoopParameters(object):
    """
    Attributes: args, main_file, tracked_files, passed_special_parameter.
    """

    def __init__(self):
        parameters = sys.argv[1:]

        # check if first parameter is a plus
        if parameters[0] == '+':
            self.passed_special_parameter = True
            parameters = parameters[1:]
        else:
            self.passed_special_parameter = False

        # get args
        for i, word in enumerate(parameters):
            if word.startswith('-'):
                self.args = ' '.join(parameters[i:])
                break
        else:  # if no break
            self.args = ''
            i += 1

        # get tracked files and main file paths
        self.tracked_files = parameters[:i]
        self.main_file = self.tracked_files[-1]


def create_if_doesnt_exist(path, template=None):
    if not exists(path):
        if template:
            templates_dir = join(dirname(realpath(__file__)), 'templates')
            template_path = join(templates_dir, template + '.txt')
            system('cp {0} {1}'.format(template_path, path))
        else:
            system('touch ' + path)


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


def open_in_editor(path):
    system('$EDITOR ' + path)
