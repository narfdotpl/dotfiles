#!/usr/bin/env python
# encoding: utf-8
"""
Check all files with JSLint and reload current Safari page.
"""

from loopozorg import Loop


def _main():
    jslint = """
        for filepath in {tracked_files}; do
            echo "****"
            echo "**** $filepath"
            echo "****"

            java -jar ~/tools/rhino.jar ~/tools/jslint.js "$filepath"

            echo
        done;
    """

    safari = """
        osascript -e '
            tell application "Safari"
                do JavaScript "window.location.reload()" in front document
            end tell
        '
    """

    Loop(jslint + safari)

if __name__ == '__main__':
    _main()
