from unittest import TestCase

from mock import MagicMock, patch
from nose.tools import raises, eq_

from pyolite.managers.user import UserManager


class TestUser(TestCase):
  @raises(ValueError)
  def test_create_user_with_no_key(self):
    with patch.multiple('pyolite.managers.manager',
                        Git=MagicMock(),
                        Path=MagicMock()):
      users = UserManager('~/path/to/admin/gitolite/repo')
      users.create('test_username')

  def test_create_user_succesfully(self):
    mocked_user = MagicMock(return_value='test_username')
    mocked_git = MagicMock()
    mocked_path = MagicMock()

    with patch.multiple('pyolite.managers.manager',
                        Git=MagicMock(return_value=mocked_git),
                        Path=MagicMock(return_value=mocked_path)):
      with patch.multiple('pyolite.managers.user', User=mocked_user):
        users = UserManager('~/path/to/admin/gitolite/repo')

        eq_('test_username', users.create('test_username', 'key_path'))
        mocked_user.assert_called_once_with(mocked_path, mocked_git,
                                            'test_username', keys=['key_path'])

  def test_get_user(self):
    mocked_user = MagicMock()
    mocked_user.get_by_name.return_value = 'test_user'

    mocked_git = MagicMock()
    mocked_path = MagicMock()

    with patch.multiple('pyolite.managers.manager',
                        Git=MagicMock(return_value=mocked_git),
                        Path=MagicMock(return_value=mocked_path)):
      with patch.multiple('pyolite.managers.user', User=mocked_user):
        users = UserManager('~/path/to/admin/gitolite/repo')

        eq_('test_user', users.get('test_user'))
        mocked_user.get_by_name.assert_called_once_with('test_user',
                                                        mocked_path,
                                                        mocked_git)
