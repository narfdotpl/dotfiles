#!/usr/bin/env python
# encoding: utf-8
"""
Proxy `open` command (<3 OS X).

If called without arguments, open working directory in Finder.  If
argument is an archive, extract it and optionally move to Trash.
"""

from itertools import imap
from os.path import isfile
from pipes import quote
from subprocess import call
from sys import argv

from move_to_trash import move_to_trash


__author__ = 'Maciej Konieczny <hello@narf.pl>'


def ask(question):
    answer = None
    while answer not in ['yes', 'y', 'no', 'n']:
        answer = raw_input(question + ' ').lower()
    return answer.startswith('y')


def call_in_the_shell(command):
    return call(command, shell=True)


def extract_archives(args):
    """
    Extract archives, pop them from the original list and optionally move
    to Trash.
    """

    # pair archive extensions with extraction commands
    tar = lambda s='': 'tar --extract --verbose {0} --file'.format(s)
    extensions_and_commads = [
        ('.tar', tar()),
        ('.tar.bz2', tar('--bzip')),  # <- order...
        ('.tar.gz', tar('--gzip')),
        ('.tgz', tar('--gzip')),
        ('.bz2', 'bunzip2'),  # <- ...matters
        ('.gz', 'gunzip'),
        ('.zip', 'unzip'),
    ]

    # extract archives and pop them from the original list
    extracted = []
    i = 0
    while i < len(args):
        path = args[i]
        popped = False
        if isfile(path):
            for extension, command in extensions_and_commads:
                if path.endswith(extension):
                    # extract
                    return_code = call_in_the_shell(command + ' ' + path)
                    if return_code == 0:
                        extracted.append(path)

                    # pop
                    args.pop(i)
                    popped = True

                    break
        if not popped:
            i += 1

    # optionally move extracted archives to trash
    if extracted:
        one_by_one = len(extracted) == 1
        if not one_by_one:
            if ask('Move all extracted archives to Trash?'):
                for archive in extracted:
                    move_to_trash(archive)
            elif ask('Move any extracted archive to Trash?'):
                one_by_one = True

        if one_by_one:
            for archive in extracted:
                if ask('Move {0} to Trash?'.format(archive)):
                    move_to_trash(archive)


def _main():
    # `list(imap(...))` is better than `map(...)`, because it's more py3ish :)
    args = list(imap(quote, argv[1:]))
    if not args:
        call_in_the_shell('open .')
    else:
        extract_archives(args)
        if args:
            call_in_the_shell('open ' + ' '.join(args))

if __name__ == '__main__':
    _main()
