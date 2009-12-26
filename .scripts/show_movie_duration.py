#!/usr/bin/env python
# encoding: utf-8
"""
Show movie duration.
"""

from itertools import ifilter
from os.path import exists
from subprocess import PIPE, Popen
from sys import argv


def get_duration(path):
    # http://superuser.com/questions/81903#81960
    command = 'ffmpeg -i {0} 2>&1 | grep Duration'.format(path)

    #   Duration: 00:27:36.90, start: 0.000000, bitrate: 1168 kb/s
    # => 00:27:36.90
    output = Popen(command, shell=True, stdout=PIPE).stdout.read()
    return output.split(',')[0].split()[-1]


def _main():
    paths = [path.replace(' ', '\ ') for path in ifilter(exists, argv[1:])]

    if not paths:
        print 'Please pass at least one valid path.'
    elif len(paths) == 1:
        print get_duration(paths[0])
    else:
        for path in paths:
            print get_duration(path), path

if __name__ == '__main__':
    _main()
