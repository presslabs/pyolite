import pytest
from mock import MagicMock, patch, call

from pyolite.models.user import User


def set_mocks():
    mocks = {}

    for mock in ['initial_path', 'path', 'file', 'keys', 'git',
                 'first_key',
                 'second_key']:
        mocks[mock] = MagicMock()

    key_path = 'tests/fixtures/second_simple_key.pub'
    mocks['second_key'].__str__ = lambda x: key_path
    mocks['second_key'].isdir.return_value = True

    key_path = 'tests/fixtures/simple_key.pub'
    mocks['first_key'].__str__ = lambda x: key_path
    mocks['first_key'].isdir.return_value = False

    mocks['file'].walk.return_value = [mocks['first_key']]
    mocks['path'].return_value = mocks['file']

    return mocks


def test_if_a_user_can_be_retrieved_by_name():
    mocks = set_mocks()

    with patch.multiple('pyolite.models.user', Path=mocks['path'],
                        ListKeys=mocks['keys']):
        user = User(mocks['initial_path'], mocks['git'], 'vtemian', repos=None,
                    keys=[mocks['first_key']])
        test_user = User.get_by_name('vtemian', mocks['initial_path'],
                                     mocks['git'])

        assert test_user.name == user.name
        assert test_user.repos == user.repos
        assert test_user.keys == user.keys
        assert test_user.path == user.path
        assert test_user.git == user.git

        mocks['path'].has_calls([
            call('path', 'keydir'),
            call('path', 'conf/')
        ])

        assert str(test_user) == '< vtemian >'
        assert repr(test_user) == '< vtemian >'


def test_if_user_is_admin():
    mocks = set_mocks()

    with patch.multiple('pyolite.models.user', Path=mocks['path'],
                        ListKeys=mocks['keys']):
        user = User(mocks['initial_path'], mocks['git'], 'vtemian', repos=None,
                    keys=[mocks['first_key']])
        assert not user.is_admin

        user.repos = ['/path/to/gitolite/admin/gitolite.conf']
        assert user.is_admin


def test_get_user_by_nothing_it_should_raise_value_error():
    mocks = set_mocks()

    with patch.multiple('pyolite.models.user', Path=mocks['path'],
                        ListKeys=mocks['keys']):
        with pytest.raises(ValueError):
            User.get(MagicMock(), mocks['git'], mocks['path'])
