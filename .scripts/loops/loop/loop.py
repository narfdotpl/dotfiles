#!/usr/bin/env python
# encoding: utf-8
"""
Run command on file modification.
"""

from itertools import imap
import os
from os import system
from os.path import exists
import stat
import sys
from time import sleep


__author__ = 'Maciej Konieczny <hello@narf.pl>'


class Loop(object):

    def __init__(self, command=None, parameters=sys.argv[1:]):
        # be pesimistic
        self.passed_special_parameter = False
        self.tracked_files = None
        self.args = ''

        # special parameter
        if parameters and parameters[0] == '+':
            self.passed_special_parameter = True
            parameters = parameters[1:]

        if parameters:
            # args
            for i, parameter in enumerate(parameters):
                if parameter.startswith('-'):
                    self.args = ' '.join(parameters[i:])
                    break
            else:  # if no break
                i += 1

            # tracked files
            self.tracked_files = parameters[:i]

        if command:
            self.run(command)

    @property
    def main_file(self):
        if self.tracked_files and isinstance(self.tracked_files, list):
            return self.tracked_files[-1]

    def run(self, command, enable_special=True):
        if enable_special and self.passed_special_parameter:
            create_file_if_it_doesnt_exist(self.main_file)

        old_mtime_sum = -1

        while True:
            new_mtime_sum = sum(imap(get_mtime, self.tracked_files))
            if old_mtime_sum != new_mtime_sum:
                old_mtime_sum = new_mtime_sum
                system('clear;' + command)
            sleep(1)  # one second


def create_file_if_it_doesnt_exist(filepath):
    if not exists(filepath):
        system('touch ' + filepath)


def get_mtime(filepath):
    return os.stat(filepath)[stat.ST_MTIME]
