[narf][]’s dotfiles
===================

Some of my configuration files and scripts used on [macOS][].
Plus installer. My keyboard config is in a [separate repo][zmk].

  [narf]: http://narf.pl
  [macOS]: http://narf.pl/posts/mac-software-2022
  [zmk]: https://github.com/narfdotpl/zmk-config


Installation
------------

Installer creates symbolic links in your `$HOME`.  It asks whether
to backup files that otherwise would be replaced.  Requires Python
and [Homebrew][].

  [Homebrew]: https://brew.sh


### Fresh

    cd ~
    git clone https://github.com/narfdotpl/dotfiles.git
    cd dotfiles
    ./install


### Update

    h
    /
    .
    g m
    ./install
