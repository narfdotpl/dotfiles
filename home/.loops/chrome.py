#!/usr/bin/env python
# encoding: utf-8
"""
Reload current Chrome tab.
"""

from loopozorg import Loop


def _main():
    Loop("""osascript -e '
        tell application "Google Chrome"
            tell the active tab of its first window
                reload
            end tell
        end tell
    '""")

if __name__ == '__main__':
    _main()
