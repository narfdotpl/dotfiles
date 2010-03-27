#!/usr/bin/env python
# encoding: utf-8
"""
Compile [Markdown][], enhance it with [SmartyPants][], add [GitHub][]
styling and show everything in [Chrome][].

  [Markdown]: http://daringfireball.net/projects/markdown/
  [SmartyPants]: http://daringfireball.net/projects/smartypants/
  [GitHub]: http://github.com/
  [Chrome]: http://google.com/chrome
"""

from subprocess import call

from loopozorg import Loop


def _main():
    # set html tempfile path
    loop = Loop()
    loop.html = '/tmp/markdown.html'

    # create empty html file and open it in chrome
    call('touch {0}; open -a "google chrome" {0}'.format(loop.html),
         shell=True)

    # compile markdown, enhance it with smartypants, add github styling and
    # refresh chrome
    loop.run("""
        echo '<!DOCTYPE html><html lang="en"><head><meta content="text/html;charset=utf-8" http-equiv="content-type"><title>Markdown preview</title><link href="http://assets1.github.com/stylesheets/bundle_common.css" rel="stylesheet"><link href="http://assets1.github.com/stylesheets/bundle_github.css" rel="stylesheet"></head><body><div class="site"><div id="files"><div class="file"><div id="readme" class="blob"><div class="wikistyle">' > {html};
        markdown {main_file} | smartypants >> {html};
        echo '</div></div></div></div></div></body></html>' >> {html};
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
