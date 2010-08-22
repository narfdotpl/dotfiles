[narfdotpl][]'s dotfiles
========================

Some of my configuration files and scripts used on OS X and Ubuntu.
Plus installer.

  [narfdotpl]: http://narf.pl/


Installation
------------

Installer creates symbolic links in your `$HOME`.  It asks whether to backup
files that otherwise would be replaced.  Requires [Python][] (2.6 <= version
< 3.0).

  [Python]: http://python.org/


### Fresh

    cd ~
    git clone git://github.com/narfdotpl/dotfiles
    cd dotfiles
    ./install


### Update

    cd ~/dotfiles
    git checkout master
    ./install
