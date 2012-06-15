#!/usr/bin/env python
# encoding: utf-8
"""
Compile [Markdown][], enhance it with [SmartyPants][], add [GitHub][]
styling and show everything in [Chrome][].

  [Markdown]: http://daringfireball.net/projects/markdown/
  [SmartyPants]: http://daringfireball.net/projects/smartypants/
  [GitHub]: https://github.com/
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

    # set bootstrap.css path
    loop.bootstrap = join(CURR_DIR, 'bootstrap.css')

    # create empty html file and open it in chrome
    call('touch {0}; open -a "google chrome" {0}'.format(loop.html),
         shell=True)

    # compile markdown, enhance it with smartypants, add github styling and
    # refresh chrome
    loop.run("""
        echo '<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Markdown preview</title><link href="{bootstrap}" rel="stylesheet"><style>.container {{ padding: 1.3em }}</style></head><body><br><div class="container"><div class="row"><div class="span6">' > {html};
        markdown {main_file} | smartypants >> {html};
        echo '</div></div></div><br></body></html>' >> {html};
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
