#!/usr/bin/env python
# encoding: utf-8
"""
Show minimal Git log.

When working on a non-master branch, show `master..branch` log.  When
working on master, show `origin..HEAD` log; if there is no origin, show
last seven commits.

Formatting example:

    * 2009-12-18 moved editor settings to one place
    * 2009-12-12 simplified references to websites

"""

from subprocess import call

from git import Git


__author__ = 'Maciej Konieczny <hello@narf.pl>'


def _main():
    git = Git()
    command = ' '.join([
        'git log',
        git.minimal_commit_range or '--max-count=7',
        '--graph --pretty=format:"%ad %s" --date=short'
    ])
    call(command, shell=True)

if __name__ == '__main__':
    _main()
