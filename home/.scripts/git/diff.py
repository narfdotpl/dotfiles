#!/usr/bin/env python
# encoding: utf-8
"""
Show (in gvim) changes from specific commit (`show <sha>` or
`show HEAD@{<n>}`) or changes in working tree relative to the latest
commit (`diff HEAD`).

Usage:

    python diff.py [<sha>/<n>]

<n> can be integer from [0; 99] range.
"""

from subprocess import call
from sys import argv, stderr

from git import Git


__author__ = 'Maciej Konieczny <hello@narf.pl>'


def validate_n(string):
    """
    If string represents integer from [0; 99] range, return this integer.
    Otherwise exit with exit code 1.
    """

    def exit_on_incorrect():
        print >> stderr, "'{0}' is not integer from [0; 99] range" \
                         .format(string)
        exit(1)

    try:
        n = int(string)
    except ValueError:
        exit_on_incorrect()
    else:
        if n < 0:
            exit_on_incorrect()

    return n


def _main():
    # stop if there's no repo
    Git()

    # parse arguments
    arguments = argv[1:]
    if not arguments:
        command = 'diff HEAD'
    else:
        argument = arguments.pop(0)
        if len(argument) <= 2:  # n
            n = validate_n(argument)
            command = 'show HEAD@{{{0}}}'.format(n)
        else:  # sha
            command = 'show ' + argument

    # show usage info if there are any arguments left
    if arguments:
        print >> stderr, __doc__[1:-1]
        exit(1)

    # just do it
    call('git {0} | gvim -R -'.format(command), shell=True)

if __name__ == '__main__':
    _main()
