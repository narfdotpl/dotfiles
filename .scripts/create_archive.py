#!/usr/bin/env python
# encoding: utf-8
"""
Archive working directory ignoring stuff that Git would ignore.  Strip
initial dot, if working directory is hidden.

Usage:

    python archive.py (tar.bz2 | zip)


Dependencies:

    - [Git], duh

 [Git]: http://git-scm.com/
"""

from os.path import basename, realpath
from sys import argv

from utils import Git, exit1, system


__author__ = 'Maciej Konieczny <hello@narf.pl>'


def _main():
    # parse command line arguments
    try:
        extension = argv[1]
    except IndexError:
        exit1(__doc__[1:-1])

    # set format
    if extension == 'tar.bz2':
        format = 'tar'
        pipe = '| bzip2'
    elif extension == 'zip':
        format = 'zip'
        pipe = ''
    else:
        exit1(__doc__[1:-1])

    # check if you are within Git repository
    try:
        Git()
    except EnvironmentError:
        no_repo = True
    else:
        no_repo = False

    # create repository
    if no_repo:
        system('git init --quiet && ' \
               'git add . && ' \
               'git commit --quiet --message="waka waka"')

    # get working directory name and strip initial dot
    directory = basename(realpath('.')).lstrip('.')

    # create archive
    archive = '{directory}.{extension}'.format(**locals())
    system('git archive --format={format} --prefix={directory}/ HEAD ' \
           '{pipe} > {archive} && echo created archive {archive}' \
           .format(**locals()))

    # remove repository
    if no_repo:
        system('rm -rf .git')

if __name__ == '__main__':
    _main()
