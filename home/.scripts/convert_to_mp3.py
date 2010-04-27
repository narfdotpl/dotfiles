#!/usr/bin/env python3
"""
Convert movies and music in other formats to mp3s.

Usage:

    python3 convert_to_mp3.py path1 [path2 ...]


The script saves mp3s in the working directory and ignores all command
line arguments that are not paths to existing files.

My ffmpeg can't do its work in silence, so I redirect both stdout and
stderr to a PIPE, that I never read.  Obviously this is not very smart
and if something goes wrong, there are no error messages -- you've been
warned!

Dependencies:

  - [FFmpeg][] (I don't know the number of the lowest version that does
    the job, I use trunk r20701)

  [FFmpeg]: http://ffmpeg.org/
"""

from datetime import datetime
from os.path import abspath, basename, exists, isfile, splitext
from pipes import quote
from subprocess import PIPE, Popen
from sys import argv, stderr, stdout


__author__ = 'Maciej Konieczny <hello@narf.pl>'


# ffmpeg has a sick number of options.  Instead of studying them, I just
# use defaults.
COMMAND = 'ffmpeg -i {infile} -f mp3 -ab 128k {outfile}'


def get_time_str():
    return datetime.now().strftime('%H:%M:%S')


def _usage():
    # strip preceding and trailing \n
    return __doc__[1:-1]


def _main():
    # get movies/music paths
    paths = list(map(quote, map(abspath, filter(isfile, argv[1:]))))
    if not paths:
        print(_usage(), file=stderr)
        exit(1)

    for path in paths:
        # set outfile name
        name = basename(path).rstrip("'")
        outfile = './{0}.mp3'.format(splitext(name)[0])

        # omit convertion if outfile already exists
        if exists(outfile):
            print('{0} omitting {1}: {2} already exists' \
                  .format(get_time_str(), name, outfile))
            continue

        # convert
        print('{0} converting {1}...'.format(get_time_str(), name), end='')
        stdout.flush()
        Popen(
            COMMAND.format(infile=path, outfile=quote(outfile)),
            shell=True, stdout=PIPE, stderr=PIPE
        ).communicate()
        print(' -> ' + outfile)

    # finish
    print('{0} finished'.format(get_time_str()))

if __name__ == '__main__':
    _main()
