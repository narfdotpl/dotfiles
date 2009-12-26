#!/usr/bin/env python
# encoding: utf-8
"""
Parse Git information for shell prompt.

Show current branch name.  If there were any changes since last commit, show
a plus sign.  If there are any stashed changes, show an ampersand.  If current
directory is not the top-level directory of the repository, precede branch name
with one dot for each directory below the top.

example:

    ~ $ cd dotfiles
    ~/dotfiles(master) $ cd .scripts
    ~/dotfiles/.scripts(.master) $ touch foo
    ~/dotfiles/.scripts(.master+) $ git add foo; git stash
    ~/dotfiles/.scripts(.master&) $

"""

from subprocess import PIPE, Popen

from git import Git


__author__ = 'Maciej Konieczny <hello@narf.pl>'


def _main():
    try:
        git = Git()
    except EnvironmentError:
        pass
    else:
        # depth
        prompt = '.' * git.depth

        # branch name
        prompt += git.branch

        # changes
        if not git.is_clean:
            prompt += '+'

        # stashed
        if Popen(['git', 'stash', 'list'], stdout=PIPE).stdout.readlines():
            prompt += '&'

        print '(' + prompt + ')',

if __name__ == '__main__':
    _main()