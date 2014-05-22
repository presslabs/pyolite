from unittest import TestCase

from mock import MagicMock, patch, call
from nose.tools import eq_

from pyolite.models.lists.users import ListUsers


class TestUserList(TestCase):
  def test_get_users(self):
    mocked_path = MagicMock()
    mocked_re = MagicMock()
    mocked_repository = MagicMock()

    mocked_user1 = MagicMock()
    mocked_user2 = MagicMock()

    mocked_user1.group.return_value = 'user1'
    mocked_user2.group.return_value = 'user2'

    mocked_path.return_value = 'tests/fixtures/repo_users.conf'
    mocked_re.compile('=( *)(\w+)').finditer.return_value = [mocked_user1,
                                                             mocked_user2]
    mocked_repository.name = 'users'

    with patch.multiple('pyolite.models.lists.users',
                        re=mocked_re, Path=mocked_path):
      repo_users = ListUsers(mocked_repository)

      eq_(repo_users._get_users(), ['user1', 'user2'])

      mocked_re.compile.has_calls([call('=( *)(\w+)')])
      mocked_re.compile('=( *)(\w+)').finditer.has_calls([call('conf')])

      mocked_user1.group.has_calls([call(1)])
      mocked_user2.group.has_calls([call(2)])

      mocked_path.assert_called_once_with(mocked_path.path, 'conf/repos/',
                                          "users.conf")
