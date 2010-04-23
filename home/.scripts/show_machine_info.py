#!/usr/bin/env python
# encoding: utf-8
"""
Show machine name, os name and uptime.

If machine name matches the first passed argument, show only uptime.

example:

    $ python show_machine_info.py
    MacBook.local (Darwin), up 61 days

    $ python show_machine_info.py MacBook.local
    up 61 days

"""

from subprocess import PIPE, Popen
from sys import argv


__author__ = 'Maciej Konieczny <hello@narf.pl>'


def read_stdout(command):
    return Popen(command, shell=True, stdout=PIPE).stdout.read().rstrip('\n')


def _main():
    name = read_stdout('uname -n')
    system = read_stdout('uname -s')

    # 21:49  up  8:49, 6 users, load averages: 0.43 0.35 0.38
    # => 8:49
    #
    #  21:52:27 up 5 days, 15:51,  1 user,  load average: 0.02, 0.03, 0.01
    # => 5 days
    uptime = ' '.join(read_stdout('uptime').split(',')[0].split()[2:])

    args = argv[1:]
    if args and args[0] == name:
        print 'up ' + uptime
    else:
        print '{name} ({system}), up {uptime}'.format(**locals())

if __name__ == '__main__':
    _main()
