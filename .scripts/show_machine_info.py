#!/usr/bin/env python
# encoding: utf-8
"""
Show machine name, os name and uptime.

example:

    MacBook.local (Darwin), up 61 days

"""

from os import popen


def main():
    with popen('uname -n') as f:
        name = f.read().rstrip('\n')

    with popen('uname -s') as f:
        os = f.read().rstrip('\n')

    with popen('uptime') as f:
        # 21:49  up  8:49, 6 users, load averages: 0.43 0.35 0.38
        # => 8:49
        #
        #  21:52:27 up 5 days, 15:51,  1 user,  load average: 0.02, 0.03, 0.01
        # => 5 days
        uptime = ' '.join(f.read().split(',')[0].split()[2:])

    print '%s (%s), up %s' % (name, os, uptime)

if __name__ == '__main__':
    main()

