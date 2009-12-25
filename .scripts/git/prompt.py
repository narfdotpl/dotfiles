#!/usr/bin/env python
# encoding: utf-8
"""
Parse Git information for shell prompt.

Show current branch name.  If there were any changes since last commit, show
a plus sign.  If current directory is not the top-level directory of the
repository, precede branch name with one dot for each directory below the top.

example:

    ~ $ cd dotfiles
    ~/dotfiles(master) $ cd .scripts
    ~/dotfiles/.scripts(.master) $ touch foo
    ~/dotfiles/.scripts(.master+) $

"""

from git import Git


__author__ = 'Maciej Konieczny <hello@narf.pl>'


def _main():
    try:
        git = Git()
    except EnvironmentError:
        pass
    else:
        prompt = '.' * git.depth
        prompt += git.branch
        if not git.is_clean:
            prompt += '+'
        print '(' + prompt + ')',

if __name__ == '__main__':
    _main()
