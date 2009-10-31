#!/usr/bin/env python
# encoding: utf-8
"""
Install dotfiles by creating symbolic links in $HOME directory.

Also remove obsolete links from previous installations and ask whether to
backup files that otherwise would be replaced.
"""

from glob import iglob
from os import listdir, readlink, remove, rename, symlink
from os.path import basename, dirname, exists, expanduser, isdir, islink, \
                    join, realpath
from shutil import rmtree


__author__ = 'Maciej Konieczny <hello@narf.pl>'


def get_already_installed(dotfiles, home_dir=None):
    """
    List links that already point at things in dotfiles directory.
    """

    home_dir = home_dir or expanduser('~')
    dotfiles_dir = dirname(dotfiles[0])

    already_installed = []
    for name in listdir(home_dir):
        path = join(home_dir, name)
        if islink(path):
            if readlink(path).startswith(dotfiles_dir):
                already_installed.append(path)
    return already_installed


def get_dotfiles(dotfiles_dir=None):
    """
    List absolute paths to dotfiles; ignore .git/, installer, readme and
    everything that matches .gitglobalignore patterns.
    """

    dotfiles_dir = dotfiles_dir or join(dirname(realpath(__file__)), '..')

    # get everything
    dotfiles_names = listdir(dotfiles_dir)

    # ignore .git/, installer and readme
    for name in ['.git', 'install', 'installer', 'README.markdown']:
        if name in dotfiles_names:
            dotfiles_names.remove(name)

    # ignore everything that matches .gitglobalignore patterns
    gitglobalignore = join(dotfiles_dir, '.gitglobalignore')
    if exists(gitglobalignore):
        with open(gitglobalignore) as f:
            for line in f:
                if line != '\n' and not line.startswith('#'):
                    pattern = line.rstrip('\n')
                    patterns = [pattern]
                    # `*foo == *foo and .*foo` in git but not in python
                    if pattern.startswith('*'):
                        patterns.append('.' + pattern)
                    for pattern in patterns:
                        for path in iglob(pattern):
                            name = basename(path)
                            if name in dotfiles_names:
                                dotfiles_names.remove(name)

    # return absolute paths
    return [join(dotfiles_dir, name) for name in dotfiles_names]


def get_fresh_and_obsolete(dotfiles, already_installed):
    fresh = _get_fresh(dotfiles, already_installed)
    obsolete = _get_obsolete(dotfiles, already_installed)
    return fresh, obsolete

def _get_fresh(dotfiles, already_installed):
    """
    List dotfiles that are not installed yet.
    """

    # create (name, path) pairs
    files = [(basename(d), d) for d in dotfiles]
    links = [(basename(link), readlink(link)) for link in already_installed]

    for link_name, destination in links:
        for i, (dotfile_name, dotfile_path) in enumerate(files):
            if link_name == dotfile_name and destination == dotfile_path:
                del files[i]
                break
    return [path for name, path in files]

def _get_obsolete(dotfiles, already_installed):
    """
    List links that do not point at proper dotfiles.
    """

    obsolete = []
    dotfiles_names = map(basename, dotfiles)
    for link in already_installed:
        name = basename(link)
        destination = readlink(link)
        if destination not in dotfiles or name not in dotfiles_names:
            obsolete.append(link)
    return obsolete


def install_and_ask_whether_to_backup(fresh, home_dir=None,
                                      forced_answer=None):
    """
    Create symbolic links in $HOME directory and ask whether to backup files
    that would be replaced. Backup by appending "~" to the name.
    """

    home_dir = home_dir or expanduser('~')

    if not fresh:
        print 'nothing fresh to install'

    for path in sorted(fresh):
        destination = join(home_dir, basename(path))
        name = _pretty_basename(path)
        installed = False
        while not installed:
            try:
                symlink(path, destination)
            except OSError:  # if destination already exists
                if forced_answer is None:
                    answer = None
                    while answer not in ['yes', 'y', 'no', 'n']:
                        answer = raw_input('backup %s? yes/no: ' % name). \
                                                                       lower()
                    backup = True if answer[0] == 'y' else False
                else:
                    backup = forced_answer

                if backup:
                    new_destination = destination + '~'
                    while exists(new_destination):
                        new_destination += '~'
                    rename(destination, new_destination)
                    print 'renamed to %s' % _pretty_basename(new_destination)
                else:
                    if isdir(destination):
                        rmtree(destination)
                    else:
                        remove(destination)
            else:
                installed = True
                print '%s installed' % name


def _pretty_basename(path):
    name = basename(path)
    if isdir(path):
        name += '/'
    return name


def uninstall(obsolete):
    """
    Remove obsolete links from previous installations.
    """

    for link in obsolete:
        remove(link)
        print '%s uninstalled' % _pretty_basename(link)


def main():
    # get all the info
    dotfiles = get_dotfiles()
    already_installed = get_already_installed(dotfiles)
    fresh, obsolete = get_fresh_and_obsolete(dotfiles, already_installed)

    # do the magic
    uninstall(obsolete)
    install_and_ask_whether_to_backup(fresh)

if __name__ == '__main__':
    main()

