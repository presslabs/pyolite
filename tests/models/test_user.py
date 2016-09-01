from unittest import TestCase

from mock import MagicMock, patch, call
from nose.tools import eq_, raises

from pyolite.models.user import User


class TestUserModel(TestCase):
    def set_mocks(self):
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

    def test_if_a_user_can_be_retrieved_by_name(self):
        mocks = self.set_mocks()

        with patch.multiple('pyolite.models.user', Path=mocks['path'],
                            ListKeys=mocks['keys']):
            user = User(mocks['initial_path'], mocks['git'], 'vtemian', [],
                        [mocks['first_key']])
            test_user = User.get_by_name('vtemian', mocks['initial_path'],
                                         mocks['git'])

            eq_(test_user.name, user.name)
            eq_(test_user.repos, user.repos)
            eq_(test_user.keys, user.keys)
            eq_(test_user.path, user.path)
            eq_(test_user.git, user.git)

            mocks['path'].has_calls([
                call('path', 'keydir'),
                call('path', 'conf/')
            ])

            eq_(str(test_user), '< vtemian >')
            eq_(repr(test_user), '< vtemian >')

    def test_if_user_is_admin(self):
        mocks = self.set_mocks()

        with patch.multiple('pyolite.models.user', Path=mocks['path'],
                            ListKeys=mocks['keys']):
            user = User(mocks['initial_path'], mocks['git'], 'vtemian', [],
                        [mocks['first_key']])
            eq_(user.is_admin, False)

            user.repos = ['/path/to/gitolite/admin/gitolite.conf']
            eq_(user.is_admin, True)

    @raises(ValueError)
    def test_get_user_by_nothing_it_should_raise_value_error(self):
        mocks = self.set_mocks()

        with patch.multiple('pyolite.models.user', Path=mocks['path'],
                            ListKeys=mocks['keys']):
            User.get(MagicMock(), mocks['git'], mocks['path'])
