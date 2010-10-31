[narfdotpl][]'s dotfiles
========================

Some of my configuration files and scripts used on OS X.
Plus installer.

  [narfdotpl]: http://narf.pl/


Glimpse
-------

![screenshot](http://dl.dropbox.com/u/2618196/dotfiles.png)


Installation
------------

Installer creates symbolic links in your `$HOME`.  It asks whether
to backup files that otherwise would be replaced.  Requires Python
(2.6 ≤ version < 3) and Git.


### Fresh

    cd ~
    git clone http://github.com/narfdotpl/dotfiles.git
    cd dotfiles
    ./install


### Update

    cd ~/dotfiles
    git checkout master
    ./install
