#!/usr/bin/env python3
"""
Convert movies to iPhone mp4s.

Usage:

    python convert_to_iphone_mp4.py moviepath1 moviepath2 ...

The script ignores all command line arguments that are not paths to
existing files.

My ffmpeg can't do its work in silence, so I redirect both stdout and
stderr to a PIPE, that I never read.  Obviously this is not very smart
and if something goes wrong, there are no error messages -- you've been
warned!

Dependencies:

  - [FFmpeg][] (I don't know the number of the lowest version that does
    the job, I use 0.5)

  [FFmpeg]: http://ffmpeg.org/
"""

from datetime import datetime
from os.path import abspath, basename, dirname, isfile, join, splitext
from pipes import quote
from re import compile, findall
from subprocess import PIPE, Popen
from sys import argv, stdout


__author__ = 'Maciej Konieczny <hello@narf.pl>'


WIDTH, HEIGHT = 480, 320
ASPECT = WIDTH / HEIGHT
FULLSCREEN_BITRATE = 1200

# ffmpeg has a sick number of options.  Instead of studying them, I just
# use defaults.
COMMAND = 'ffmpeg -i {infile} -f mp4 -b {bitrate}k -ab 128k ' \
          '-s {width}x{height} {outfile}'


def usage():
    print(__doc__.lstrip('\n').rstrip('\n'))


def compute_bitrate(width, height):
    area = width * height
    max_area = WIDTH * HEIGHT
    return int(FULLSCREEN_BITRATE * area / max_area)


def get_time_str():
    return datetime.now().strftime('%H:%M:%S')


def multiple_of_16(integer):
    return int(round(integer / 16)) * 16


def _main():
    # get movie paths
    paths = list(map(quote, map(abspath, filter(isfile, argv[1:]))))
    if not paths:
        usage()
        exit()

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
        directory = dirname(path)
        name = basename(path)
        new_name = '{0}.iphone.mp4'.format(splitext(name)[0])
        outfile = join(directory, new_name)

        # convert
        print('{0} converting {1}...'.format(get_time_str(), name), end='')
        stdout.flush()
        Popen(COMMAND.format(
            infile=path,
            outfile=outfile,
            width=width,
            height=height,
            bitrate=compute_bitrate(width, height)
        ), shell=True, stdout=PIPE, stderr=PIPE).communicate()
        print('-> ' + new_name)

    # finish
    print('{0} finished'.format(get_time_str()))

if __name__ == '__main__':
    _main()
