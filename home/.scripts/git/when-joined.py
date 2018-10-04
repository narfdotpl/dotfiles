#!/usr/bin/env python
# encoding: utf-8
"""
Get date of each committer's first commit (in whole repo or just
for <path>).

Usage:

    python when-joined.py [<path>]

<path> has to be relative to repo root.
"""

from pipes import quote
from subprocess import PIPE, Popen
from sys import argv, stderr

from git import Git


__author__ = 'Maciej Konieczny <hello@narf.pl>'


def _main():
    # stop if there's no repo
    Git()

    # show usage info if there are too many arguments
    if len(argv) > 2:
        print >> stderr, __doc__[1:-1]
        exit(1)

    # get <path>
    if len(argv) == 2:
        path = quote(argv[1])
    else:
        path = ''

    # get ready
    accessions = {}  # {'author': 'date'}
    command = 'git log --reverse --pretty=format:"%ad %an" --date=short ' + \
              path

    # read one commit at a time
    for line in Popen(command, shell=True, stdout=PIPE).stdout:
        split = line.split()
        date = split[0]
        author = ' '.join(split[1:])

        if author not in accessions:
            accessions[author] = date

    # list authors in chronological order
    for author, date in sorted(accessions.items(), key=lambda tpl: tpl[1]):
        print date, author

if __name__ == '__main__':
    _main()
