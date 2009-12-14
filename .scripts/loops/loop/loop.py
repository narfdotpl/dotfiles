#!/usr/bin/env python
# encoding: utf-8
"""
Run command on file modification.
"""

import sys


__author__ = 'Maciej Konieczny <hello@narf.pl>'


class Loop(object):

    def __init__(self, parameters=sys.argv[1:]):
        # be pesimistic
        self.passed_special_parameter = False
        self.tracked_files = None
        self.main_file = None
        self.args = None

        # special parameter
        if parameters and parameters[0] == '+':
            self.passed_special_parameter = True
            parameters = parameters[1:]

        # quit if there is nothing left to parse
        if not parameters:
            return

        # args
        for i, parameter in enumerate(parameters):
            if parameter.startswith('-'):
                self.args = ' '.join(parameters[i:])
                break
        else:  # if no break
            i += 1

        # tracked files and main file
        self.tracked_files = parameters[:i]
        self.main_file = self.tracked_files[-1]
