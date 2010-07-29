#!/usr/bin/env python
# encoding: utf-8
"""
Show movie duration.

Usage:

    python show_movie_duration.py <path> [<other paths>]

The script ignores all command line arguments that are not paths to
existing files.

Dependencies:

  - [FFmpeg][] (I don't know the number of the lowest version that does
    the job, I use 0.5)

  [FFmpeg]: http://ffmpeg.org/
"""

from itertools import ifilter, imap
from os.path import isfile
from pipes import quote
from subprocess import PIPE, Popen
from sys import argv

from utils import exit1


__author__ = 'Maciej Konieczny <hello@narf.pl>'


def get_duration(path):
    # http://superuser.com/questions/81903#81960
    command = 'ffmpeg -i {0} 2>&1 | grep Duration'.format(path)

    #   Duration: 00:27:36.90, start: 0.000000, bitrate: 1168 kb/s
    # => 00:27:36.90
    output = Popen(command, shell=True, stdout=PIPE).stdout.read()
    return output.split(',')[0].split()[-1]


def _main():
    # get movie paths
    # `list(imap(...))` is better than `map(...)`, because it's more py3ish :)
    paths = list(imap(quote, ifilter(isfile, argv[1:])))
    if not paths:
        exit1(__doc__[1:-1])

    if len(paths) == 1:
        print get_duration(paths[0])
    else:
        for path in paths:
            print get_duration(path), path

if __name__ == '__main__':
    _main()
