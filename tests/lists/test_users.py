from spec import Spec

from mock import MagicMock, patch
from nose.tools import eq_, raises

from pyolite.models.lists.users import ListUsers


class TestUserList(Spec):
  @raises(ValueError)
  def test_if_we_add_invalid_permissions_it_should_raise_ValueError(self):
    mocked_path = MagicMock()
    mocked_re = MagicMock()
    mocked_repository = MagicMock()
    mocked_user = MagicMock()

    mocked_user.name = 'another_user'

    mocked_path.return_value = 'tests/fixtures/users.conf'
    mocked_re.compile('=( *)(\w+)').findall.return_value = [(None, 'user')]

    with patch.multiple('pyolite.models.lists.users',
                        Path=mocked_path, re=mocked_re):
      repo_users = ListUsers(mocked_repository)
      repo_users.add('test', 'hiRW+')

  def test_it_should_add_a_new_user_to_repo_if_is_valid(self):
    mocked_path = MagicMock()
    mocked_re = MagicMock()
    mocked_repository = MagicMock()
    mocked_user = MagicMock()

    mocked_user.name = 'another_user'
    mocked_user.__str__ = lambda x: 'another_user'
    mocked_repository.name = 'test_repo'

    mocked_path.return_value = 'tests/fixtures/users.conf'
    mocked_re.compile('=( *)(\w+)').findall.return_value = [(None, 'user')]

    _get_users = ListUsers._get_users
    _get_user = ListUsers._get_user
    ListUsers._get_users = lambda x: []
    ListUsers._get_user = lambda x, user: mocked_user
    with patch.multiple('pyolite.models.lists.users',
                        Path=mocked_path, re=mocked_re):
      repo_users = ListUsers(mocked_repository)
      repo_users.add('test', 'RW+')

      with open('tests/fixtures/users.conf', 'r+') as f:
        content = f.read()
        f.seek(0)
        f.write('')
        f.truncate()

      eq_(content, "    RW+     =    another_user\n")
      message = 'User another_user added to repo test_repo ' \
                'with permissions: RW+'
      mocked_repository.git.commit.assert_called_once_with(['conf'], message)

    ListUsers._get_users = _get_users
    ListUsers._get_user = _get_user

  def test_user_permission_edit(self):
    mocked_path = MagicMock()
    mocked_re = MagicMock()
    mocked_repository = MagicMock()
    mocked_user = MagicMock()

    mocked_user.name = 'another_user'
    mocked_user.__str__ = lambda x: 'another_user'
    mocked_repository.name = 'test_repo'

    mocked_path.return_value = 'tests/fixtures/users.conf'
    mocked_re.compile('=( *)(\w+)').findall.return_value = [(None, 'user')]

    _get_users = ListUsers._get_users
    _get_user = ListUsers._get_user
    ListUsers._get_users = lambda x: []
    ListUsers._get_user = lambda x, user: mocked_user
    with patch.multiple('pyolite.models.lists.users',
                        Path=mocked_path, re=mocked_re):
      repo_users = ListUsers(mocked_repository)
      repo_users.add('test', 'RW+')

      with open('tests/fixtures/users.conf', 'r+') as f:
        content = f.read()
        f.seek(0)
        f.write('')
        f.truncate()

      eq_(content, "    RW+     =    another_user\n")
      message = 'User another_user added to repo test_repo ' \
                'with permissions: RW+'
      mocked_repository.git.commit.assert_called_once_with(['conf'], message)

    ListUsers._get_users = _get_users
    ListUsers._get_user = _get_user


