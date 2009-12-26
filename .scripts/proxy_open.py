#!/usr/bin/env python
# encoding: utf-8
"""
Proxy `open` command.

If called without arguments, open working directory in finder.  If argument is an archive, extract it.
"""

from os.path import isfile
from subprocess import call
from sys import argv


__author__ = 'Maciej Konieczny <hello@narf.pl>'


def _main():
    args = argv[1:]

    if args:
        for i, arg in enumerate(args):
            if isfile(arg):
                for extension, command in [
                    ('.tar', 'tar xvf'),
                    ('.tar.bz2', 'tar xvjf'),  # <- order...
                    ('.tar.gz', 'tar xvzf'),
                    ('.tgz', 'tar xvzf'),
                    ('.bz2', 'bunzip2'),  # <- ...matters
                    ('.gz', 'gunzip'),
                    ('.zip', 'unzip'),
                ]:
                    if arg.endswith(extension):
                        call(command + ' ' + arg, shell=True)
                        args.pop(i)
                        break

        if args:
            command = 'open ' + ' '.join(args)
    else:
        command = 'open .'

    call(command, shell=True)

if __name__ == '__main__':
    _main()
