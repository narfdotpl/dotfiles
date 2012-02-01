#!/usr/bin/env python
# encoding: utf-8
"""
Read commit's diff, find submodule changes and generate "compare links"
for modules hosted on GitHub.

Usage:

    python get-compare-links.py [<sha>]

HEAD is default SHA.
"""

from os.path import exists, join
from subprocess import PIPE, Popen
from sys import argv, stderr

from git import Git


__author__ = 'Maciej Konieczny <hello@narf.pl>'


class Submodule(object):

    def __init__(self, fs_path, git_url):
        self.path = fs_path
        self.url = git_url[:-len('.git')]

    @property
    def compare_link(self):
        return '{}/compare/{}'.format(self.url, self.rng)

def get_submodules(f):
    submodules = []
    path = url = None
    for line in f:
        if path is None and line.strip().startswith('path'):
            path = line.split()[-1]
        elif url is None and line.strip().startswith('url'):
            url = line.split()[-1]

        if path and url:
            if 'github.com' in url:
                submodules.append(Submodule(path, url))
            path = url = None

    return submodules


def _main():
    # stop if there's no repo
    git = Git()

    # read .gitmodules from repo root
    repo_dir = join('.', *(['..'] * git.depth))
    path = join(repo_dir, '.gitmodules')
    if exists(path):
        with open(path) as f:
            submodules_by_path = {x.path: x for x in get_submodules(f)}
    else:
        print >> stderr, '.gitmodules not found'
        exit(1)

    # get sha
    if len(argv) == 2:
        sha = argv[-1]
    else:
        sha = 'HEAD'

    # get commit shas from `git show`
    updated_submodules = []
    path = rng = None
    process = Popen('git show ' + sha, shell=True, stdout=PIPE)
    process.wait()
    for line in process.stdout:
        if path is None:
            if line.startswith('diff --git a/'):
                path = line.split()[2][2:]
        elif rng is None:
            if line.startswith('index'):
                rng = line.split()[1].replace('..', '...')

        if path and rng:
            submodule = submodules_by_path[path]
            submodule.rng = rng
            updated_submodules.append(submodule)
            path = rng = None

    # print links
    for submodule in sorted(updated_submodules, key=lambda x: x.url):
        print submodule.compare_link

if __name__ == '__main__':
    _main()
