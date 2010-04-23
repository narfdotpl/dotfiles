#!/usr/bin/env python
# encoding: utf-8
"""
Reload current Chrome tab.
"""

from loopozorg import Loop


def _main():
    Loop("""osascript -e '
        tell application "Google Chrome"
            activate
            tell application "System Events"
                keystroke "r" using command down
                keystroke tab using command down
            end tell
        end tell
    '""")

if __name__ == '__main__':
    _main()
