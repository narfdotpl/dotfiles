#!/usr/bin/env python
# encoding: utf-8
"""
A set of functions used across different scripts.  Scripts import
functions from this module, not from each other.
"""

from subprocess import call
from sys import stderr


__author__ = 'Maciej Konieczny <hello@narf.pl>'


def exit1(message):
    print >> stderr, message
    exit(1)


def system(command):
    return call(command, shell=True)


def which(app):
    """
    `which $app`
    """

    return_code = call('which {0} > /dev/null'.format(app), shell=True)
    return return_code == 0


# scripts import from this module, not from each other
from move_to_trash import move_to_trash
from quicklook import preview
