#!/usr/bin/env python
# encoding: utf-8
"""
Reload current Safari page.
"""

from loop import Loop


def _main():
    Loop("""osascript -e '
        tell application "Safari"
            do JavaScript "window.location.reload()" in front document
        end tell
    '""")

if __name__ == '__main__':
    _main()
