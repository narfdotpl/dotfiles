#!/usr/bin/env python
# encoding: utf-8
"""
Work with Git branches using one command.

Usage:

    python branch.py [<branch name>|<other arguments>]

Act as an alias, unless called with one argument: assume then it's a
branch name and try to checkout it; if it doesn't exist, ask whether to
create it.
"""

from subprocess import PIPE, Popen, call
from sys import argv

from git import Git


__author__ = 'Maciej Konieczny <hello@narf.pl>'


def _main():
    # stop if there's no repo
    Git()

    # get args
    if len(argv) == 2:
        branch = argv[1]
        args = None
    else:
        args = ' '.join(argv[1:])

    # do the magic
    if args is not None:
        call('git branch ' + args, shell=True)
    else:
        message = Popen(
            'git checkout ' + branch, shell=True, stderr=PIPE
        ).stderr.read().rstrip('\n')

        if 'did not match' in message:
            print "Branch '{0}' doesn't exist.".format(branch),

            answer = None
            while answer not in ['yes', 'y', 'no', 'n']:
                answer = raw_input('Create it? ').lower()

            if answer.startswith('y'):
                call('git checkout -b ' + branch, shell=True)
        elif message:
            print message

if __name__ == '__main__':
    _main()
