#!/usr/bin/env python
# encoding: utf-8
"""
Compile and run .asm file any time it's modified. Remove everything but
source afterwards.
"""

import re

from baseloop import get_files_and_args, loop


def main():
    tracked_files, main_file, args = get_files_and_args()
    out = re.sub(r'\.asm$', '.o', main_file)
    bin = re.sub(r'\.asm$', '', main_file)
    command = ';'.join([
        'nasm -f macho -o %s %s -DMAC' % (out, main_file),
        'ld -o %s %s' % (bin, out),
        './%s' % bin,
        'rm %s %s' % (bin, out)
    ])
    loop(tracked_files, command)

if __name__ == '__main__':
    main()

