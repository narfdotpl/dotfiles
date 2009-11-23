#!/usr/bin/env python
# encoding: utf-8
"""
Print `top` table trimmed to four heaviest processes ordered by CPU usage and
copy to the clipboard command killing the heaviest one.
"""

import os


def main():
    how_many = 4

    # get list of processes ordered by CPU usage (ascending)
    with os.popen('top -l 2 -o +cpu') as f:
        top = f.readlines()

    # get valid line numbers (trim `top` table to `how_many` processes)
    first_row_id = 7
    stop = length = len(top)
    start = length - how_many
    if start <= first_row_id:  # if how_many is too many
        start = first_row_id + 1
    line_numbers = [first_row_id]
    line_numbers.extend(range(start, stop))

    # print trimmed `top` table
    for i in line_numbers:
        print top[i],

    # copy to clipboard command killing the heaviest process
    pid, name, cpu = top[-1].split()[:3]
    os.system(
        'echo -n "kill {0}  # {1} ({2} CPU)" | pbcopy'.format(pid, name, cpu)
    )

if __name__ == '__main__':
    main()

