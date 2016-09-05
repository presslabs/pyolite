from unittest import TestCase

from mock import MagicMock, patch
from nose.tools import eq_

from pyolite.repo import Repo


class TestRepo(TestCase):
    def test_it_should_replace_a_given_string_in_repo_conf(self):
        mocked_re = MagicMock()
        path = 'tests/fixtures/config.conf'

        mocked_re.sub.return_value = 'another_text'

        with patch.multiple('pyolite.repo', re=mocked_re):
            repo = Repo(path)
            repo.replace('pattern', 'string')

            with open('tests/fixtures/config.conf') as f:
                eq_(f.read(), 'another_text')

            mocked_re.sub.assert_called_once_with('pattern', 'string',
                                                  'another_text')

    def test_it_should_retrieve_all_users_from_repo(self):
        path = 'tests/fixtures/repo_users.conf'
        mocked_path = MagicMock()
        mocked_path.__str__ = lambda x: path

        mocked_path.exists.return_value = True

        mocked_re = MagicMock()
        mocked_user1 = MagicMock()
        mocked_user2 = MagicMock()

        mocked_re.compile('=( *)(\w+)').finditer.return_value = [mocked_user1,
                                                                 mocked_user2]
        mocked_user1.group.return_value = 'user1'
        mocked_user2.group.return_value = 'user2'

        with patch.multiple('pyolite.repo', re=mocked_re):
            repo = Repo(mocked_path)
            eq_(repo.users, ['user1', 'user2'])

    def test_it_should_write_to_repo_config(self):
        path = 'tests/fixtures/empty_repo.conf'

        Repo(path).write('some_text')

        with open(path, 'r+') as f:
            eq_('some_text', f.read())

            f.seek(0)
            f.write('')
            f.truncate()

    def test_it_should_overwrite_the_repo_config(self):
        path = 'tests/fixtures/empty_repo.conf'

        Repo(path).write('some_text')

        Repo(path).overwrite('another_text')

        with open(path, 'r+') as f:
            eq_('another_text', f.read())

            f.seek(0)
            f.write('')
            f.truncate()

    def test_replace_filelocking(self):
        mocked_re = MagicMock()
        mocked_fcntl = MagicMock()

        mocked_open = MagicMock()
        path = 'tests/fixtures/config.conf'

        with patch('__builtin__.open', mocked_open):
            manager = mocked_open.return_value.__enter__.return_value

            # asserts file locking has been put in place before reading
            manager.read = lambda: ([
                mocked_fcntl.flock.assert_called_once_with(
                    manager, mocked_fcntl.LOCK_EX
                ),
                mocked_fcntl.reset_mock()
            ])

            with patch.multiple('pyolite.repo', re=mocked_re,
                                fcntl=mocked_fcntl):
                repo = Repo(path)

                mocked_fcntl.reset_mock()
                repo.replace('pattern', 'string')

                # asserts lock has been removed after operating on file
                mocked_fcntl.flock.assert_called_once_with(manager,
                                                           mocked_fcntl.LOCK_UN)

    def test_users_filelocking(self):
        path = 'tests/fixtures/repo_users.conf'
        mocked_path = MagicMock()
        mocked_path.__str__ = lambda x: path

        mocked_path.exists.return_value = True

        mocked_re = MagicMock()
        mocked_fcntl = MagicMock()
        mocked_open = MagicMock()

        with patch('__builtin__.open', mocked_open):
            manager = mocked_open.return_value.__enter__.return_value

            # asserts file locking has been put in place before reading
            manager.read = lambda: ([
                mocked_fcntl.flock.assert_called_once_with(
                    manager, mocked_fcntl.LOCK_EX
                ),
                mocked_fcntl.reset_mock()
            ])

            with patch.multiple('pyolite.repo', re=mocked_re,
                                fcntl=mocked_fcntl):
                repo = Repo(mocked_path)

                mocked_fcntl.reset_mock()
                repo.users

                # asserts lock has been removed after reading
                mocked_fcntl.flock.assert_called_once_with(manager,
                                                           mocked_fcntl.LOCK_UN)

    def test_write_filelocking(self):
        path = 'tests/fixtures/empty_repo.conf'
        mocked_path = MagicMock()
        mocked_path.__str__ = lambda x: path

        mocked_fcntl = MagicMock()
        mocked_open = MagicMock()

        with patch('__builtin__.open', mocked_open):
            manager = mocked_open.return_value.__enter__.return_value

            # asserts file locking has been put in place before writing
            manager.write = lambda text: ([
                mocked_fcntl.flock.assert_called_once_with(
                    manager, mocked_fcntl.LOCK_EX
                ),
                mocked_fcntl.reset_mock()
            ])

            with patch.multiple('pyolite.repo', fcntl=mocked_fcntl):
                repo = Repo(path)

                mocked_fcntl.reset_mock()
                repo.write('some_text')

                # asserts lock has been removed after writing
                mocked_fcntl.flock.assert_called_once_with(manager,
                                                           mocked_fcntl.LOCK_UN)

    def test_overwrite_filelocking(self):
        path = 'tests/fixtures/empty_repo.conf'
        mocked_path = MagicMock()
        mocked_path.__str__ = lambda x: path

        mocked_fcntl = MagicMock()
        mocked_open = MagicMock()

        with patch('__builtin__.open', mocked_open):
            manager = mocked_open.return_value.__enter__.return_value

            # asserts file locking has been put in place before writing
            manager.write = lambda text: ([
                mocked_fcntl.flock.assert_called_once_with(
                    manager, mocked_fcntl.LOCK_EX
                ),
                mocked_fcntl.reset_mock()
            ])

            with patch.multiple('pyolite.repo', fcntl=mocked_fcntl):
                repo = Repo(path)

                mocked_fcntl.reset_mock()
                repo.overwrite('some_text')

                # asserts lock has been removed after writing
                mocked_fcntl.flock.assert_called_once_with(manager,
                                                           mocked_fcntl.LOCK_UN)
