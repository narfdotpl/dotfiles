#!/usr/bin/env python3
"""
Convert movies to iPhone mp4s.

Usage:

    python3 convert_to_iphone_mp4.py <path> [<other paths>]

The script saves mp4s in the working directory and ignores all command
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
from re import compile, findall
from subprocess import PIPE, Popen
from sys import argv, stderr, stdout


__author__ = 'Maciej Konieczny <hello@narf.pl>'


WIDTH, HEIGHT = 480, 320
ASPECT = WIDTH / HEIGHT
FULLSCREEN_BITRATE = 1200

# ffmpeg has a sick number of options.  Instead of studying them, I just
# use defaults.
COMMAND = 'ffmpeg -i {infile} -f mp4 -b {bitrate}k -ab 128k ' \
          '-s {width}x{height} {outfile}'


def _compute_bitrate(width, height):
    area = width * height
    max_area = WIDTH * HEIGHT
    return int(FULLSCREEN_BITRATE * area / max_area)


def get_time_str():
    return datetime.now().strftime('%H:%M:%S')


def multiple_of_16(integer):
    return int(round(integer / 16)) * 16


def _usage():
    # strip preceding and trailing \n
    return __doc__[1:-1]


def _main():
    # get movie paths
    paths = list(map(quote, map(abspath, filter(isfile, argv[1:]))))
    if not paths:
        print(_usage(), file=stderr)
        exit(1)

    # (width, height)
    pattern = compile(r'(\d+)x(\d+)')

    for path in paths:
        # get size of the original video
        command = 'ffmpeg -i {0} 2>&1 | grep Video'.format(path)
        output = Popen(command, shell=True, stdout=PIPE).stdout.read().decode()
        width, height = map(int, findall(pattern, output)[0])

        # adjust size if it's bigger than the screen
        aspect = width / height
        if aspect >= ASPECT:
            if width > WIDTH:
                width = WIDTH
                height = multiple_of_16(width / aspect)
        else:
            if height > HEIGHT:
                height = HEIGHT
                width = multiple_of_16(height * aspect)

        # set outfile name
        name = basename(path).rstrip("'")
        outfile = './{0}.iphone.mp4'.format(splitext(name)[0])

        # omit convertion if outfile already exists
        if exists(outfile):
            print('{0} omitting {1}: {2} already exists' \
                  .format(get_time_str(), name, outfile))
            continue

        # convert
        print('{0} converting {1}...'.format(get_time_str(), name), end='')
        stdout.flush()
        Popen(COMMAND.format(
            infile=path,
            outfile=quote(outfile),
            width=width,
            height=height,
            bitrate=_compute_bitrate(width, height)
        ), shell=True, stdout=PIPE, stderr=PIPE).communicate()
        print(' -> ' + outfile)

    # finish
    print('{0} finished'.format(get_time_str()))

if __name__ == '__main__':
    _main()
