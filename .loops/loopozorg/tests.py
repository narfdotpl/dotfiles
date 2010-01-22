# encoding: utf-8
"""
Test suite.

Run with nose http://somethingaboutorange.com/mrl/projects/nose
"""

from os.path import isfile, join
from shutil import rmtree
from tempfile import mkdtemp
from time import sleep

from nose.tools import assert_equals, raises

from loopozorg import Loop, create_file_if_it_doesnt_exist, \
                      _get_caller_filename, get_mtime, open_file_in_editor


__author__ = 'Maciej Konieczny <hello@narf.pl>'


class TestAttributes:

    def test_all_clean_on_clean_init(self):
        loop = Loop(parameters=[])
        for actual, expected in [
            (loop.raw, ''),
            (loop.passed_special, False),
            (loop.tracked_files, []),
            (loop.main_file, ''),
            (loop.args, ''),
        ]:
            assert_equals(actual, expected)

    def test_all_parsed_correctly(self):
        # prepare parameters
        parameters = ['+']  # passed_special = True
        tracked_files = ['foo', 'bar']
        parameters.extend(tracked_files)
        main_file = tracked_files[-1]
        args = '-3 --verbose reset --hard'
        parameters.extend(args.split())

        loop = Loop(parameters=parameters)
        for actual, expected in [
            (loop.raw, ' '.join(parameters)),
            (loop.passed_special, True),
            (loop.tracked_files, tracked_files),
            (loop.main_file, main_file),
            (loop.args, args),
        ]:
            assert_equals(actual, expected)

    def test_format_attributes(self):
        expected = {
            'raw': 'foo bar baz --waka -waka waka',
            'passed_special': 'False',
            'tracked_files': 'foo bar baz',
            'main_file': 'baz',
            'args': '--waka -waka waka',
        }
        loop = Loop(parameters=
            expected['tracked_files'].split() \
            + expected['args'].split()
        )
        actual = loop._get_attrs_as_dict_of_strs()
        assert_equals(actual, expected)

    def test_backslash_parameters(self):
        expected = 'foo\ bar baz'
        actual = Loop(parameters=['foo bar', 'baz']) \
                 ._get_attrs_as_dict_of_strs()['raw']
        assert_equals(actual, expected)

    def test_backslash_paths(self):
        loop = Loop(parameters=['some file', 'main file'])
        attrs = loop._get_attrs_as_dict_of_strs()
        for key, expected in [
            ('tracked_files', 'some\ file main\ file'),
            ('main_file', 'main\ file'),
        ]:
            actual = attrs[key]
            assert_equals(actual, expected)

    def test_user_defined_attributes(self):
        loop = Loop(parameters=[])
        loop.foo = None

        expected = 'None'
        actual = loop._get_attrs_as_dict_of_strs()['foo']

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


    def test_dont_create_file_if_it_already_exists(self):
        # create test file
        filepath = join(self.directory, 'foo')
        with open(filepath, 'w'):
            pass
        mtime_before = get_mtime(filepath)
        sleep(1)  # one second

        create_file_if_it_doesnt_exist(filepath)
        mtime_after = get_mtime(filepath)

        assert_equals(mtime_before, mtime_after)

    def test_create_file_if_it_doesnt_exist(self):
        filepath = join(self.directory, 'foo')
        create_file_if_it_doesnt_exist(filepath)
        assert isfile(filepath), 'File not created'

    def test_use_template(self):
        template = join(self.directory, 'template')
        content = 'waka waka waka'
        with open(template, 'w') as f:
            f.write(content)

        filepath = join(self.directory, 'foo')
        create_file_if_it_doesnt_exist(filepath, template)

        with open(filepath) as f:
            assert_equals(f.read(), content)

    def test_caller_name(self):
        assert_equals(_get_caller_filename(), 'nosetests')


class TestOpenFile:

    @raises(EnvironmentError)
    def test_raise_exception_if_EDIT_is_not_set(self):
        open_file_in_editor(filepath=None, edit='')
