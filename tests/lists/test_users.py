from spec import Spec

from mock import MagicMock, patch, call
from nose.tools import raises
from pyolite.models.lists.users import ListUsers


class TestUserList(Spec):
  @raises(ValueError)
  def test_it_should_raise_ValueError_if_user_exists_when_we_add_him(self):
    mocked_repo = MagicMock()
    mocked_repository = MagicMock()
    mocked_user = MagicMock()

    mocked_user.get.return_value = MagicMock(name='another_user')
    mocked_repo.users = ['another_user']

    with patch.multiple('pyolite.models.lists.users',
                        Repo=mocked_repo, User=mocked_user):
      repo_users = ListUsers(mocked_repository)
      repo_users.add('test', 'hiRW+')

  @raises(ValueError)
  def test_if_we_add_invalid_permissions_it_should_raise_ValueError(self):
    mocked_repo = MagicMock()
    mocked_repository = MagicMock()
    mocked_user = MagicMock()

    mocked_user.get.return_value = MagicMock(name='another_user')
    mocked_repo.users = ['user']

    with patch.multiple('pyolite.models.lists.users',
                        Repo=mocked_repo, User=mocked_user):
      repo_users = ListUsers(mocked_repository)
      repo_users.add('test', 'hiRW+')

  def test_it_should_add_a_new_user_to_repo_if_is_valid(self):
    mocked_repo = MagicMock()
    mocked_repository = MagicMock()
    mocked_user = MagicMock()

    mock_single_user = MagicMock()
    mock_single_user.name = 'another_user'
    mock_single_user.__str__ = lambda x: 'another_user'

    mocked_repository.name = 'test_repo'

    mocked_user.get.return_value = mock_single_user
    mocked_repo.users = ['user']

    with patch.multiple('pyolite.models.lists.users',
                        Repo=MagicMock(return_value=mocked_repo),
                        User=mocked_user):
      repo_users = ListUsers(mocked_repository)
      repo_users.add('test', 'RW+')

      content = '    RW+     =    another_user\n'
      mocked_repo.write.assert_called_once_with(content)

      message = 'User another_user added to repo test_repo ' \
                'with permissions: RW+'
      mocked_repository.git.commit.has_calls([call(['conf'], message)])

  def test_user_removing(self):
    mocked_repo = MagicMock()
    mocked_repository = MagicMock()
    mocked_user = MagicMock()

    mock_single_user = MagicMock()
    mock_single_user.name = 'another_user'
    mock_single_user.__str__ = lambda x: 'another_user'

    mocked_repository.name = 'test_repo'

    mocked_user.get.return_value = mock_single_user
    mocked_repo.users = ['user']

    with patch.multiple('pyolite.models.lists.users',
                        Repo=MagicMock(return_value=mocked_repo),
                        User=mocked_user):
      repo_users = ListUsers(mocked_repository)
      repo_users.remove('test')

      pattern = r'(\s*)([RW+DC]*)(\s*)=(\s*)%s' % 'another_user'
      mocked_repo.replace.assert_called_once_with(pattern, "")

      message = "Deleted user another_user from repository test_repo"
      mocked_repository.git.commit.has_calls([call(['conf'], message)])

  def test_user_edit_permissions(self):
    mocked_repo = MagicMock()
    mocked_repository = MagicMock()
    mocked_user = MagicMock()

    mock_single_user = MagicMock()
    mock_single_user.name = 'another_user'
    mock_single_user.__str__ = lambda x: 'another_user'

    mocked_repository.name = 'test_repo'

    mocked_user.get.return_value = mock_single_user
    mocked_repo.users = ['user']

    with patch.multiple('pyolite.models.lists.users',
                        Repo=MagicMock(return_value=mocked_repo),
                        User=mocked_user):
      repo_users = ListUsers(mocked_repository)
      repo_users.edit('test', 'R')

      pattern = r'(\s*)([RW+DC]*)(\s*)=(\s*)%s' % 'another_user'
      string = r"\n    %s    =    %s" % ('R', 'another_user')
      mocked_repo.replace.assert_called_once_with(pattern, string)

      message = "User another_user has R permission for repository test_repo"
      mocked_repository.git.commit.has_calls([call(['conf'], message)])
