from unittest import TestCase

from mock import MagicMock, patch, call
from nose.tools import eq_, raises

from pyolite.models.lists.users import ListUsers
from pyolite.models.user import User


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

  def test_get_user_if_user_is_string(self):
    mocked_git = MagicMock()
    mocked_path = MagicMock()
    mocked_repository = MagicMock()

    class MockUser(User):
      @classmethod
      def get_by_name(cls, user, path, repo):
        return my_user

    my_user = MockUser(mocked_path, mocked_git, 'vlad',
                       keys=['tests/fixtures/simple_key.pub'])

    _get_users = ListUsers._get_users
    ListUsers._get_users = lambda x: []
    with patch.multiple('pyolite.models.lists.users',
                        Path=mocked_path,
                        User=MockUser):
      repo_users = ListUsers(mocked_repository)

      eq_(repo_users._get_user('user'), my_user)
    ListUsers._get_users = _get_users

  def test_replace_in_repo_config(self):
    mocked_path = MagicMock()
    mocked_re = MagicMock()
    mocked_repository = MagicMock()

    mocked_path.return_value = 'tests/fixtures/config.conf'
    mocked_re.sub.return_value = 'another_text'

    _get_users = ListUsers._get_users
    ListUsers._get_users = lambda x: []
    with patch.multiple('pyolite.models.lists.users',
                        Path=mocked_path, re=mocked_re):
      repo_users = ListUsers(mocked_repository)
      repo_users._replace_in_repo('pattern', 'string')

      with open('tests/fixtures/config.conf') as f:
        eq_(f.read(), 'another_text')

    ListUsers._get_users = _get_users

  def test_add_existing_user_in_repo(self):
    mocked_path = MagicMock()
    mocked_re = MagicMock()
    mocked_repository = MagicMock()
    mocked_user = MagicMock()

    mocked_user.name = 'user'

    mocked_path.return_value = 'tests/fixtures/users.conf'
    mocked_re.compile('=( *)(\w+)').findall.return_value = [(None, 'user')]

    _get_users = ListUsers._get_users
    _get_user = ListUsers._get_user
    ListUsers._get_users = lambda x: []
    ListUsers._get_user = lambda x, user: mocked_user
    with patch.multiple('pyolite.models.lists.users',
                        Path=mocked_path, re=mocked_re):
      repo_users = ListUsers(mocked_repository)

      try:
        repo_users.add('test', 'RW+')
      except ValueError:
        ListUsers._get_users = _get_users
        ListUsers._get_user = _get_user
