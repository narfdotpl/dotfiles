# encoding: utf-8
"""
Test suite.

Run with nose http://somethingaboutorange.com/mrl/projects/nose
"""

from os import system
from os.path import exists, join
from shutil import rmtree
from tempfile import mkdtemp
from time import sleep

from nose.tools import assert_equals, raises

from loop import Loop, create_file_if_it_doesnt_exist, get_mtime, \
                 open_file_in_editor


class TestDefaultParameters:

    def test_get_all_clean_on_clean_init(self):
        loop = Loop(parameters=[])
        for actual, expected in [
            (loop.passed_special_parameter, False),
            (loop.tracked_files, None),
            (loop.main_file, None),
            (loop.args, ''),
        ]:
            assert_equals(actual, expected)

    def test_get_all_properly_parsed(self):
        # prepare parameters
        parameters = ['+']  # passed_special_parameter = True
        tracked_files = ['foo', 'bar']
        parameters.extend(tracked_files)
        main_file = tracked_files[-1]
        args = '-3 --verbose reset --hard'
        parameters.extend(args.split())

        loop = Loop(parameters=parameters)
        for actual, expected in [
            (loop.passed_special_parameter, True),
            (loop.tracked_files, tracked_files),
            (loop.main_file, main_file),
            (loop.args, args),
        ]:
            assert_equals(actual, expected)


class TestCreateFile:

    def setup(self):
        """
        Make temporary directory.
        """

        self.directory = mkdtemp()

    def teardown(self):
        """
        Remove temporary directory.
        """

        rmtree(self.directory)


    def test_dont_create_file(self):
        # create test target
        filepath = join(self.directory, 'foo')
        system('touch ' + filepath)
        mtime_before = get_mtime(filepath)
        sleep(1)  # one second

        create_file_if_it_doesnt_exist(filepath)
        mtime_after = get_mtime(filepath)

        assert_equals(mtime_before, mtime_after)

    def test_create_file(self):
        target = join(self.directory, 'foo')
        create_file_if_it_doesnt_exist(target)
        assert exists(target), 'File not created'


class TestOpenFile:

    @raises(EnvironmentError)
    def test_raise_exception_if_EDIT_is_not_set(self):
        open_file_in_editor(filepath=None, edit='')
