#!/usr/bin/env python
# encoding: utf-8
"""
Convert English text to audible speech using Google Translate
text-to-speech service.

Usage:

    python google_say.py <words>

"""

from os.path import isfile
from sys import argv
from urllib import urlencode
from urllib2 import Request, urlopen

from utils import exit1, system, which


__author__ = 'Maciej Konieczny <hello@narf.pl>'


def download_mp3(mp3_path, phrase):
    url = 'http://translate.google.com/translate_tts' \
          '?' + urlencode({'q': phrase})
    agent = 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_2; en-US) ' \
            'AppleWebKit/532.9 (KHTML, like Gecko) ' \
            'Chrome/5.0.307.11 Safari/532.9'
    request = Request(url, headers={'User-Agent': agent})

    with open(mp3_path, 'w') as mp3:
        response = urlopen(request)  # I CAN HAS __EXIT__?
        for chunk in response:
            mp3.write(chunk)
        response.close()


def _main():
    # parse command line arguments
    phrase = ' '.join(argv[1:])
    if not phrase:
        exit1(__doc__[1:-1])

    # set paths
    base = '/tmp/google_say'
    mp3_path = base + '.mp3'
    txt_path = base + '.txt'

    # check if mp3 is not already downloaded
    cached = False
    if isfile(mp3_path) and isfile(txt_path):
        with open(txt_path) as f:
            old_phrase = f.read()
        cached = phrase == old_phrase

    # download mp3 and save phrase
    if not cached:
        download_mp3(mp3_path, phrase)
        with open(txt_path, 'w') as f:
            f.write(phrase)

    # try to play mp3
    if which('afplay'):
        system('afplay ' + mp3_path)
    else:
        print 'listen to ' + mp3_path

if __name__ == '__main__':
    _main()
