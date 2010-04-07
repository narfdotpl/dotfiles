#!/usr/bin/env python
# encoding: utf-8
"""
Show three trailing components of current path (replace $HOME with ~),
Git prompt, and dollar sign.
"""

from os.path import expanduser
from sys import argv

from utils import git_prompt


__author__ = 'Maciej Konieczny <hello@narf.pl>'


def prompt(path):
    prompt = simple_path(path, 3)

    git = git_prompt()
    if git:
        prompt += '({0})'.format(git)

    prompt += ' $ '
    return prompt


def simple_path(path, limit=0):
    """
    Replace $HOME with ~ and limit path to given number of trailing
    components.
    """

    home = expanduser('~')
    if path.startswith(home):
        path = path.replace(home, '~', 1)

    if limit:
        components = path.split('/')
        how_many = len(components)
        if components[0] == '':
            how_many -= 1

        if how_many > limit:
            path = '/'.join(components[-limit:])

    return path


def _main():
    # unfortunately os.getcwd, os.path.abspath and friends eliminate symlinks
    pwd = argv[1]
    print prompt(pwd)

if __name__ == '__main__':
    _main()
