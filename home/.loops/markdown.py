#!/usr/bin/env python
# encoding: utf-8
"""
Compile [Markdown][], enhance it with [SmartyPants][], add [naif.css][]
stylesheet and show everything in [Chrome][].

  [Markdown]: http://daringfireball.net/projects/markdown/
  [SmartyPants]: http://daringfireball.net/projects/smartypants/
  [naif.css]: http://lab.narf.pl/naif.css/
  [Chrome]: http://google.com/chrome
"""

from subprocess import call
from os.path import dirname, join, realpath

from loopozorg import Loop


CURR_DIR = dirname(realpath(__file__))


def _main():
    # set html tempfile path
    loop = Loop()
    loop.html = '/tmp/markdown.html'

    # set naif.css path
    loop.css = join(CURR_DIR, 'naif.css', 'naif.min.css')

    # create empty html file and open it in chrome
    call('touch {0}; open -a "google chrome" {0}'.format(loop.html),
         shell=True)

    # compile markdown, enhance it with smartypants, use naif.css and
    # refresh chrome
    loop.run("""
        echo '<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Markdown preview</title><link href="{css}" rel="stylesheet"></head><body><div id="main-wrapper">' > {html};
        markdown {main_file} | smartypants >> {html};
        echo '</div></body></html>' >> {html};
        osascript -e '
            tell application "Google Chrome"
                activate
                tell application "System Events"
                    keystroke "r" using command down
                    keystroke tab using command down
                end tell
            end tell
        '
    """)

if __name__ == '__main__':
    _main()
