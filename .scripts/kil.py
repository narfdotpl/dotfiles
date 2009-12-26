#!/usr/bin/env python
# encoding: utf-8
"""
Print `top` table trimmed to four heaviest processes ordered by CPU usage and
copy to the clipboard command killing the heaviest one.
"""

from subprocess import PIPE, Popen, call


__author__ = 'Maciej Konieczny <hello@narf.pl>'


def _main():
    how_many = 4

    # get list of processes ordered by CPU usage (ascending)
    top = Popen('top -l 2 -o +cpu', shell=True, stdout=PIPE).stdout.readlines()

    # get line numbers (trim `top` table to `how_many` processes)
    first_row_line_number = 7
    stop = len(top)
    start = stop - how_many
    if start <= first_row_line_number:  # if how_many is too many
        start = first_row_line_number + 1
    line_numbers = [first_row_line_number]
    line_numbers.extend(range(start, stop))

    # print trimmed table
    for i in line_numbers:
        print top[i],

    # copy to clipboard command killing the heaviest process
    pid, name, cpu = top[-1].split()[:3]
    call('echo -n "kill {pid}  # {name} ({cpu} CPU)" | pbcopy' \
         .format(**locals()), shell=True)

if __name__ == '__main__':
    _main()
