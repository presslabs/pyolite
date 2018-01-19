from mock import MagicMock, patch

from pyolite.repo import Repo


def test_it_should_replace_a_given_string_in_repo_conf():
    mocked_re = MagicMock()
    path = 'tests/fixtures/config.conf'

    mocked_re.sub.return_value = 'another_text'

    with patch.multiple('pyolite.repo', re=mocked_re):
        repo = Repo(path)
        repo.replace('pattern', 'string')

        with open('tests/fixtures/config.conf') as f:
            assert f.read() == 'another_text'

        mocked_re.sub.assert_called_once_with('pattern', 'string',
                                              'another_text')


def test_it_should_retrieve_all_users_from_repo():
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
        assert repo.users == ['user1', 'user2']


def test_it_should_write_to_repo_config():
    path = 'tests/fixtures/empty_repo.conf'

    Repo(path).write('some_text')

    with open(path, 'r+') as f:
        assert f.read() == 'some_text'

        f.seek(0)
        f.write('')
        f.truncate()


def test_setting_config_will_not_overwrite_users():
    path = 'tests/fixtures/empty_repo.conf'

    Repo(path).write('''
repo test-repo
    RW+   =    @support
    R     =    gitweb
    config test = testconfig
''')

    Repo(path).write_config("    config another = anotherconfig\n")

    with open(path, 'r+') as f:
        assert f.read() == '''
repo test-repo
    RW+   =    @support
    R     =    gitweb

    config another = anotherconfig
'''

        f.seek(0)
        f.write('')
        f.truncate()


def test_it_should_overwrite_the_repo_config():
    path = 'tests/fixtures/empty_repo.conf'

    Repo(path).write('some_text')

    Repo(path).overwrite('another_text')

    with open(path, 'r+') as f:
        assert f.read() == 'another_text'

        f.seek(0)
        f.write('')
        f.truncate()


def test_replace_filelocking():
    mocked_re = MagicMock()
    mocked_fcntl = MagicMock()

    mocked_open = MagicMock()
    path = 'tests/fixtures/config.conf'

    with patch('pyolite.repo.open', mocked_open, create=True):
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


def test_users_filelocking():
    path = 'tests/fixtures/repo_users.conf'
    mocked_path = MagicMock()
    mocked_path.__str__ = lambda x: path

    mocked_path.exists.return_value = True

    mocked_re = MagicMock()
    mocked_fcntl = MagicMock()
    mocked_open = MagicMock()

    with patch('pyolite.repo.open', mocked_open, create=True):
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


def test_write_filelocking():
    path = 'tests/fixtures/empty_repo.conf'
    mocked_path = MagicMock()
    mocked_path.__str__ = lambda x: path

    mocked_fcntl = MagicMock()
    mocked_open = MagicMock()

    with patch('pyolite.repo.open', mocked_open, create=True):
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


def test_overwrite_filelocking():
    path = 'tests/fixtures/empty_repo.conf'
    mocked_path = MagicMock()
    mocked_path.__str__ = lambda x: path

    mocked_fcntl = MagicMock()
    mocked_open = MagicMock()

    with patch('pyolite.repo.open', mocked_open, create=True):
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
