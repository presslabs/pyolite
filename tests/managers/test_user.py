from unittest import TestCase

from mock import MagicMock, patch
from nose.tools import raises, eq_

from pyolite.managers.user import UserManager
from tests.mocked_manager import MockManager, mocked_git, mocked_path


class TestUserManager(TestCase):
  @raises(ValueError)
  def test_create_user_with_no_key(self):
    with patch.multiple('pyolite.managers.manager',
                        Git=MagicMock(),
                        Path=MagicMock()):
      users = UserManager('~/path/to/admin/gitolite/repo')
      users.create('test_username')

  def test_create_user_succesfully(self):
    mocked_user = MagicMock(return_value='test_username')

    UserManager.__bases__ = (MockManager, )
    with patch.multiple('pyolite.managers.user', User=mocked_user,
                        Manager=MagicMock()):
      users = UserManager('~/path/to/admin/gitolite/repo')

      eq_('test_username', users.create('test_username', 'key_path'))
      mocked_user.assert_called_once_with(mocked_path, mocked_git,
                                          'test_username', keys=['key_path'])

  def test_get_user(self):
    mocked_user = MagicMock()
    mocked_user.get_by_name.return_value = 'test_user'

    UserManager.__bases__ = (MockManager, )
    with patch.multiple('pyolite.managers.user', User=mocked_user):
      users = UserManager('~/path/to/admin/gitolite/repo')

      eq_('test_user', users.get('test_user'))
      mocked_user.get_by_name.assert_called_once_with('test_user',
                                                      mocked_path,
                                                      mocked_git)

  def test_get_all_users(self):
    mocked_user = MagicMock()
    mocked_user.get_by_name.return_value = 'test_user'

    UserManager.__bases__ = (MockManager, )
    with patch.multiple('pyolite.managers.user', User=mocked_user):
      UserManager('~/path/to/admin/gitolite/repo')
