#!/usr/bin/env python
# encoding: utf-8
"""
Parse Git information for shell prompt.

Usage:

    python prompt.py

Show current branch name.  If there were any changes since last commit,
show a plus sign.  If there are any stashed changes, show an ampersand.
If current directory is not the toplevel directory of the repository,
precede branch name with one dot for each directory below the top.

Example:

    ~ $ cd dotfiles
    ~/dotfiles(master) $ cd .scripts
    ~/dotfiles/.scripts(.master) $ touch foo
    ~/dotfiles/.scripts(.master+) $ git add foo; git stash
    ~/dotfiles/.scripts(.master&) $

"""

from subprocess import PIPE, Popen
from sys import argv, stderr

from git import Git


__author__ = 'Maciej Konieczny <hello@narf.pl>'


def prompt():
    try:
        git = Git()
    except EnvironmentError:
        return ''

    # initial space
    prompt = ' '

    # depth
    prompt += '.' * git.depth

    # branch name
    prompt += git.branch

    # changes
    if not git.is_clean:
        prompt += '+'

    # stash
    if Popen('git stash list', shell=True, stdout=PIPE).stdout.readlines():
        prompt += '&'

    return prompt


def _main():
    # show usage info if there any arguments
    if len(argv) > 1:
        print >> stderr, __doc__[1:-1]
        exit(1)

    # show parsed git info
    print prompt()

if __name__ == '__main__':
    _main()
