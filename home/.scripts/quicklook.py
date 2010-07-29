#!/usr/bin/env python
# encoding: utf-8
"""
Invoke the OS X Quick Look preview from the command line.

Usage:

    python quicklook.py <path> [<other paths>]


This process is blocking.  To terminate it, press any key or close the
preview window.  Pressing space or escape closes the preview window.
"""

from pipes import quote
from subprocess import PIPE, Popen
from sys import argv
from threading import Thread
from time import sleep

from utils import exit1


__author__ = 'Maciej Konieczny <hello@narf.pl>'


def preview(item):
    QuietPopen = lambda command: Popen(command, shell=True, stdout=PIPE)

    # spawn processes
    preview_process = QuietPopen('qlmanage -p ' + item)
    keypress_process = QuietPopen("""
        read -sn 1 c
        c=$(echo $c | od -t x1 | awk '{print $2}')

        # space
        [[ $c == "0a" ]] && exit 0

        # escape
        [[ $c == "1b" ]] && exit 0

        # else
        exit 1
    """)

    # create threads
    threads = []
    interval = 0.05  # in seconds

    def wait_for_keypress():
        # wait for process to terminate
        while keypress_process.poll() is None:
            sleep(interval)

        # close preview window, if user pressed space
        if keypress_process.returncode == 0:
            preview_process.terminate()

    keypress_thread = Thread(target=wait_for_keypress)
    threads.append(keypress_thread)

    def wait_for_window_close():
        # wait for process to terminate
        while preview_process.poll() is None:
            sleep(interval)

        # stop waiting for keypress
        if keypress_process.poll() is None:
            keypress_process.terminate()

    preview_thread = Thread(target=wait_for_window_close)
    preview_thread.daemon = True
    threads.append(preview_thread)

    # start threads
    for thread in threads:
        thread.start()

    # wait till one thread terminates
    while all(thread.is_alive() for thread in threads):
        sleep(interval)


def _main():
    item = ' '.join(map(quote, argv[1:]))
    if not item:
        exit1(__doc__[1:-1])

    preview(item)

if __name__ == '__main__':
    _main()
