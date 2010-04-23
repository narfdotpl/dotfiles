#!/usr/bin/env python
# encoding: utf-8
"""
Download file showing only its name, total size and progress bar.

Usage:

    python download.py url [url ...]

"""

from subprocess import PIPE, Popen
from sys import argv

from utils import exit1, system


__author__ = 'Maciej Konieczny <hello@narf.pl>'


def get_size(url):
    size = ''
    command = 'curl --location --head -q ' + url

    for line in Popen(command, shell=True, stdout=PIPE, stderr=PIPE).stdout:
        if line.startswith('content-length'):
            size = int(line.split()[1])
            break

    # make size human-readable
    if size:
        if size < 2e5:
            size = '{0} kB'.format(round(size / 1e3))
        else:
            size = '{0} MB'.format(round(size / 1e6, 1))

    return size


def _main():
    urls = argv[1:]
    if not urls:
        exit1(__doc__[1:-1])

    for url in urls:
        # show info
        info = url.split('/')[-1]  # filename
        size = get_size(url)
        if size:
            info += ' ({0})'.format(size)
        print info

        # download showing progress bar
        system('curl --location --progress-bar --remote-name ' + url)

if __name__ == '__main__':
    _main()
