#!/usr/bin/env python
# encoding: utf-8
"""
Show minimal Git log.

When working on a non-master branch, show `master..branch` log.  When working
on master, show `origin..HEAD` log; if there is no origin, show last seven
commits.

Formatting example:

    * 2009-12-18 moved editor settings to one place
    * 2009-12-12 simplified references to websites

"""

from os import popen, system


__author__ = 'Maciej Konieczny <hello@narf.pl>'


def get_branch():
    with popen('git branch 2> /dev/null') as f:
        for line in f:
            if line.startswith('*'):
                return line[len('* '):-len('\n')]


def has_origin():
    with popen('git remote') as f:
        return 'origin\n' in f


def _main():
    branch = get_branch()
    if branch:
        if branch != 'master':
            log_range = 'master..' + branch
        else:
            log_range = 'origin..HEAD' if has_origin() else '--max-count=7'

        system('git log {0} --graph --pretty=format:"%ad %s" --date=short' \
               .format(log_range))

if __name__ == '__main__':
    _main()
