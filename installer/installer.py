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


HOME_DIR = expanduser('~')
REPO_DIR = realpath(join(dirname(__file__), '..'))
DOTFILES_DIR = join(REPO_DIR, 'home')


def get_already_installed(dotfiles, home_dir=None, repo_dir=None):
    """
    List links that already point at things in dotfiles directory.
    """

    home_dir = home_dir or HOME_DIR
    repo_dir = repo_dir or REPO_DIR
    already_installed = []

    for name in listdir(home_dir):
        path = join(home_dir, name)
        if islink(path) and readlink(path).startswith(repo_dir):
            already_installed.append(path)

    return already_installed


def get_dotfiles(dotfiles_dir=None):
    """
    List absolute paths to dotfiles.

    Ignore everything that matches .gitglobalignore patterns.
    """

    dotfiles_dir = dotfiles_dir or DOTFILES_DIR

    # get everything
    dotfiles_names = listdir(dotfiles_dir)

    # ignore everything that matches .gitglobalignore patterns
    gitglobalignore = join(dotfiles_dir, '.gitfiles/global-ignore')
    if exists(gitglobalignore):
        with open(gitglobalignore) as f:
            for line in f:
                if line != '\n' and not line.startswith('#'):
                    pattern = line.rstrip('\n')
                    patterns = [pattern]

                    # use git smart wildcards
                    if pattern.startswith('*'):
                        patterns.append('.' + pattern)  # *a == *a and .*a
                    if pattern.startswith('*.'):
                        patterns.append(pattern[1:])  # *.b == *.b and .b

                    for pattern in patterns:
                        for path in iglob(join(dotfiles_dir, pattern)):
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
    List dotfiles that are not installed (linked) yet.
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

    dotfiles_names = map(basename, dotfiles)
    obsolete = []

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
    that would be replaced.

    Backup by appending "~" to the name.
    """

    home_dir = home_dir or HOME_DIR

    for path in sorted(fresh):
        destination = join(home_dir, basename(path))
        name = _pretty_basename(path)
        installed = False

        while not installed:
            try:
                symlink(path, destination)
            except OSError:  # if destination already exists
                if forced_answer is not None:
                    backup = forced_answer
                else:
                    answer = None
                    while answer not in ['yes', 'y', 'no', 'n']:
                        answer = raw_input(
                            'backup {0}? '.format(name)
                        ).lower()
                    backup = answer.startswith('y')

                if backup:
                    suffix = '~'
                    new_destination = destination + suffix
                    while exists(new_destination):
                        new_destination += suffix
                    rename(destination, new_destination)

                    new_name = _pretty_basename(new_destination)
                    print '{0} -> {1}'.format(name, new_name)
                else:
                    if isdir(destination) and not islink(destination):
                        rmtree(destination)
                    else:
                        remove(destination)

                    print '- ' + name
            else:
                installed = True
                print '+ ' + name

    if fresh:
        print 'symlinking complete, consider restarting terminal'
    else:
        print 'nothing fresh to symlink'


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
        name = _pretty_basename(link)
        print '- ' + name


def _main():
    # get all info
    dotfiles = get_dotfiles()
    already_installed = get_already_installed(dotfiles)
    fresh, obsolete = get_fresh_and_obsolete(dotfiles, already_installed)

    # do the magic
    uninstall(obsolete)
    install_and_ask_whether_to_backup(fresh)

if __name__ == '__main__':
    _main()
