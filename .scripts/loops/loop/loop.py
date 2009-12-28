#!/usr/bin/env python
# encoding: utf-8
"""
Execute shell command on file modification.
"""

from inspect import stack
from itertools import imap
import os
from os.path import basename, dirname, isfile, join, realpath, splitext
from shutil import copy
import stat
from subprocess import PIPE, Popen, call
import sys
from time import sleep


__author__ = 'Maciej Konieczny <hello@narf.pl>'


class Loop(object):

    def __init__(self, command=None, parameters=sys.argv[1:]):
        # be pesimistic
        self.passed_special = False
        self.tracked_files = None
        self.args = ''

        # special
        if parameters and parameters[0] == '+':
            self.passed_special = True
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

    def run(self, command, template=None, enable_autotemplate=True,
            enable_special=True):
        if enable_special and self.passed_special:
            if enable_autotemplate and template is None:
                templates_dir = realpath(join(
                    dirname(__file__), '../templates'
                ))
                caller_filename = _get_caller_filename()
                template_filename = splitext(caller_filename)[0] + '.txt'
                template = join(templates_dir, template_filename)

            create_file_if_it_doesnt_exist(self.main_file, template)
            open_file_in_editor(self.main_file)

        old_mtime_sum = -1

        while True:
            new_mtime_sum = sum(imap(get_mtime, self.tracked_files))
            if old_mtime_sum != new_mtime_sum:
                old_mtime_sum = new_mtime_sum
                call('clear;' + command, shell=True)
            sleep(1)  # one second


def create_file_if_it_doesnt_exist(filepath, template=None):
    if template is not None and isfile(template) and not isfile(filepath):
        copy(template, filepath)
    else:
        with open(filepath, 'a'):
            pass


def _get_caller_filename():
    return basename(stack()[-1][1])


def get_mtime(filepath):
    return os.stat(filepath)[stat.ST_MTIME]


def open_file_in_editor(filepath, edit=None):
    """
    Open file in editor.

    Use environment variable $EDIT.  It should be set according to $EDITOR and
    should open editor in background -- $EDITOR usually opens editor in
    foreground, which holds the loop.
    """

    if edit is None:
        edit = Popen('echo -n "$EDIT"', shell=True, stdout=PIPE).stdout.read()

    if edit:
        call(edit + ' ' + filepath, shell=True)
    else:
        docstring_line_number = stack()[0][2] - 11
        raise EnvironmentError(
            'Environment variable $EDIT not set; see {0}, line {1}' \
            .format(__file__, docstring_line_number)
        )
