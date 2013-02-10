#!/usr/bin/env python
# encoding: utf-8
"""

    $ echo foo bar | title
    Foo Bar

"""

import sys


if __name__ == '__main__':
    for line in sys.stdin:
        print line.title(),
