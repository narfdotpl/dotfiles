#!/usr/bin/env python
# encoding: utf-8
"""
`Git` class for easy writing small scripts that require information like
name of current branch of git repository they are executed from.
"""

from os.path import dirname
from subprocess import PIPE, Popen


__author__ = 'Maciej Konieczny <hello@narf.pl>'


class Git(object):
    """
    Provide attributes with information about current git repository.

    All attributes really work like methods.  Yes, it is missleading, but
    this class is intended to be used in really small scripts.  It feels
    better to use `git.branch` there rather than `git.get_branch()`.
    """

    def __init__(self):
        """
        Quietly run `git status` to check if git repository is available.
        """

        process = Popen('git status', shell=True, stderr=PIPE, stdout=PIPE)
        return_code = process.wait()
        error = process.stderr.read()
        if error:
            raise EnvironmentError(return_code, error)

    @property
    def branch(self):
        """
        Get name of current branch.
        """

        for line in Popen('git branch', shell=True, stdout=PIPE).stdout:
            if line.startswith('*'):
                return line.lstrip('* ').rstrip('\n')

    @property
    def depth(self):
        """
        Get "subdirectorisness" level of current directory.

        Toplevel directory of the repository, `repo/`, is level 0.
        `repo/foo/` is level 1, and so on.
        """

        level = 0
        prefix = Popen('git rev-parse --show-prefix', shell=True,
                       stdout=PIPE).stdout.read().rstrip('/\n')

        while prefix:
            prefix = dirname(prefix)
            level += 1

        return level

    @property
    def has_origin(self):
        return 'origin\n' in Popen('git remote', shell=True,
                                   stdout=PIPE).stdout

    @property
    def is_clean(self):
        return 'clean' in Popen('git status', shell=True,
                                stdout=PIPE).stdout.readlines()[-1]

    @property
    def minimal_commit_range(self):
        """
        Try to return `master..branch` or `origin..HEAD`.
        """

        commit_range = None

        branch = self.branch
        if branch != 'master':
            commit_range = 'master..' + branch
        elif self.has_origin:
            commit_range = 'origin..HEAD'

        return commit_range
