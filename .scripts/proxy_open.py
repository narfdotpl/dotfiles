#!/usr/bin/env python
# encoding: utf-8
"""
Proxy `open` command.

If called without arguments, open working directory in finder.  If
argument is an archive, extract it.
"""

from itertools import imap
from os.path import isfile
from pipes import quote
from subprocess import call
from sys import argv


__author__ = 'Maciej Konieczny <hello@narf.pl>'


def extract_archives(args):
    tar = lambda s='': 'tar --extract --verbose {0} --file'.format(s)

    for i, path in enumerate(args):
        if isfile(path):
            for extension, command in [
                ('.tar', tar()),
                ('.tar.bz2', tar('--bzip')),  # <- order...
                ('.tar.gz', tar('--gzip')),
                ('.tgz', tar('--gzip')),
                ('.bz2', 'bunzip2'),  # <- ...matters
                ('.gz', 'gunzip'),
                ('.zip', 'unzip'),
            ]:
                if path.endswith(extension):
                    call(command + ' ' + path, shell=True)
                    args.pop(i)
                    break


def _main():
    # `list(imap(...))` is better than `map(...)`, because it's more py3ish :)
    args = list(imap(quote, argv[1:]))
    extract_archives(args)
    call('open ' + (' '.join(args) or '.'), shell=True)

if __name__ == '__main__':
    _main()
