#!/usr/bin/env python
# encoding: utf-8
"""
Compile [Markdown][], enhance it with [SmartyPants][], add [GitHub][]
styling and show everything in [Safari][].

  [Markdown]: http://daringfireball.net/projects/markdown/
  [SmartyPants]: http://daringfireball.net/projects/smartypants/
  [GitHub]: http://github.com/
  [Safari]: http://apple.com/safari/
"""

from subprocess import call

from loopozorg import Loop


def _main():
    # set html tempfile path
    loop = Loop()
    loop.html = '/tmp/markdown.html'

    # touch html file and open it in safari
    call('touch {0}; open -a safari {0}'.format(loop.html), shell=True)

    # compile markdown, enhance it with smartypants, add github styling and
    # refresh safari
    loop.run("""
        echo '<!DOCTYPE html><html lang="en"><head><meta content="text/html;charset=utf-8" http-equiv="content-type"><title>Markdown preview</title><link href="http://assets1.github.com/stylesheets/bundle_common.css" rel="stylesheet"><link href="http://assets1.github.com/stylesheets/bundle_github.css" rel="stylesheet"></head><body><div class="site"><div id="files"><div class="file"><div id="readme" class="blob"><div class="wikistyle">' > {html};
        markdown {main_file} | smartypants >> {html};
        echo '</div></div></div></div></div></body></html>' >> {html};
        osascript -e '
            tell application "Safari"
                do JavaScript "window.location.reload()" in front document
            end tell
        '
    """)

if __name__ == '__main__':
    _main()
