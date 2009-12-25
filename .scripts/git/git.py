#!/usr/bin/env python
# encoding: utf-8
"""
`Git` class for easy writing small scripts that require information like
current branch name of git repository they are executed from.
"""

from subprocess import PIPE, Popen


__author__ = 'Maciej Konieczny <hello@narf.pl>'


class Git(object):
    """
    Provide attributes with information about current git repository.

    All attributes really work like methods.  Yes, it is missleading, but this
    class is intended to be used in really small scripts and it feels better
    to use `git.branch` there rather than `git.get_branch()`.
    """

    def __init__(self):
        """
        Quietly run `git status` to check if git repository is available.
        """

        process = Popen(['git', 'status'], stderr=PIPE, stdout=PIPE)
        return_code = process.wait()
        error = ''.join(process.stderr.readlines())
        if error:
            raise EnvironmentError(return_code, error)

    @property
    def branch(self):
        """
        Get current branch name.
        """

        for line in Popen(['git', 'branch'], stdout=PIPE).stdout:
            if line.startswith('*'):
                return line.lstrip('* ').rstrip('\n')

    @property
    def has_origin(self):
        return 'origin\n' in Popen(['git', 'remote'], stdout=PIPE).stdout

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
