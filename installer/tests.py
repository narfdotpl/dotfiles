# encoding: utf-8
"""
Test suite for dotfiles installer.
"""

from os import listdir, mkdir, symlink
from os.path import basename, islink, join
from shutil import rmtree
import tempfile
from tempfile import NamedTemporaryFile as NTF

from nose.tools import assert_equals

from installer import get_already_installed, get_dotfiles, _get_fresh, \
                      _get_obsolete, install_and_ask_whether_to_backup, \
                      uninstall


def assert_no_difference(seq1, seq2):
    difference = list(set(seq1).symmetric_difference(set(seq2)))
    return assert_equals(difference, [])


class TestContainer:

    def setup(self):
        """
        Fake dotfiles and $HOME directories. Name groups of files after
        functions' output to avoid choosing files manually in each test.
        """

        # dotfiles
        # ========
        self.dotfiles_dir = tempfile.mkdtemp()

        how_many_dotfiles = 6
        random_dotfiles = [
            NTF(dir=self.dotfiles_dir, delete=False)
            for i in range(how_many_dotfiles)
        ]
        self.dotfiles = [f.name for f in random_dotfiles]

        # create ignored stuff (installer and readme)
        for filename in ['.git', 'install', 'installer', 'README.markdown']:
            with open(join(self.dotfiles_dir, filename), 'w') as f:
                pass

        # $HOME
        # =====
        self.home_dir = tempfile.mkdtemp()

        how_many_homefiles = 4
        random_homefiles = [
            NTF(dir=self.home_dir, delete=False)
            for i in range(how_many_homefiles)
        ]

        # divide dotfiles into three groups
        one_third = how_many_dotfiles // 3
        first_group = self.dotfiles[:one_third]
        second_group = self.dotfiles[one_third:-one_third]
        third_group = self.dotfiles[-one_third:]

        # don't symlink the first group and don't use the second group to
        # create correct links
        self.fresh = first_group + second_group

        self.already_installed = []
        self.obsolete = []

        obsolete_dir = join(self.home_dir, basename(self.dotfiles[0]))
        mkdir(obsolete_dir)

        # create incorrect symlinks
        for dotfile in second_group:
            # inexistent dotfile, correct name
            dotfile_name = basename(dotfile)
            inexistent_dotfile = join(self.dotfiles_dir, dotfile_name[-3:])
            destination = join(self.home_dir, dotfile_name)
            self.obsolete.append(destination)
            symlink(inexistent_dotfile, destination)
        for dotfile in third_group:
            # valid dotfile, incorrect name
            incorrect_name = ''.join(reversed(basename(dotfile)))
            destination = join(self.home_dir, incorrect_name)
            self.obsolete.append(destination)
            symlink(dotfile, destination)
        self.already_installed.extend(self.obsolete)

        # create correct symlinks
        for dotfile in third_group:
            destination = join(self.home_dir, basename(dotfile))
            self.already_installed.append(destination)
            symlink(dotfile, destination)

    def teardown(self):
        """
        Remove fake directories and files.
        """

        for directory in [self.dotfiles_dir, self.home_dir]:
            rmtree(directory)

    def get_homefiles(self):
        return [join(self.home_dir, name) for name in listdir(self.home_dir)]


    def test_get_already_installed(self):
        expected = self.already_installed
        already_installed = get_already_installed(self.dotfiles, self.home_dir)
        assert_no_difference(already_installed, expected)

    def test_get_dotfiles(self):
        expected = self.dotfiles
        dotfiles = get_dotfiles(self.dotfiles_dir)
        assert_no_difference(dotfiles, expected)

    def test__get_fresh(self):
        expected = self.fresh
        fresh = _get_fresh(self.dotfiles, self.already_installed)
        assert_no_difference(fresh, expected)

    def test__get_obsolete(self):
        expected = self.obsolete
        obsolete = _get_obsolete(self.dotfiles, self.already_installed)
        assert_no_difference(obsolete, expected)

    def test_install_and_backup(self):
        expected = self.get_homefiles()
        new_links = []
        for path in self.fresh:
            new_path = join(self.home_dir, basename(path))
            new_links.append(new_path)
            while new_path in expected:
                new_path += '~'
            expected.append(new_path)

        install_and_ask_whether_to_backup(self.fresh, self.home_dir, True)
        homefiles = self.get_homefiles()
        assert_no_difference(homefiles, expected)

        for link in new_links:
            assert islink(link)

    def test_install_without_backup(self):
        expected = self.get_homefiles()
        new_links = []
        for path in self.fresh:
            new_path = join(self.home_dir, basename(path))
            new_links.append(new_path)
            if new_path not in expected:
                expected.append(new_path)

        install_and_ask_whether_to_backup(self.fresh, self.home_dir, False)
        homefiles = self.get_homefiles()
        assert_no_difference(homefiles, expected)

        for link in new_links:
            assert islink(link)

    def test_uninstall(self):
        homefiles = self.get_homefiles()
        expected = list(set(homefiles).difference(set(self.obsolete)))
        uninstall(self.obsolete)
        whats_left = self.get_homefiles()
        assert_no_difference(whats_left, expected)

