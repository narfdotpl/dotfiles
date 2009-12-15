# encoding: utf-8
"""
Test suite.

Run with nose http://somethingaboutorange.com/mrl/projects/nose
"""

from nose.tools import assert_equals

from loop import Loop


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
