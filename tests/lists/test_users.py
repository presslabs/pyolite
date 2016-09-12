from mock import MagicMock, patch, call
from nose.tools import raises
from pyolite.models.user import User
from spec import Spec

from pyolite.models.lists.users import ListUsers


class TestUserList(Spec):
    @raises(ValueError)
    def test_it_should_raise_ValueError_if_user_exists_when_we_add_him(self):
        mocked_repo = MagicMock()
        mocked_repository = MagicMock()
        mocked_user = MagicMock()

        mocked_repository.name = 'test_repo'
        mocked_repository.path = 'path'

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

        mocked_repository.name = 'test_repo'
        mocked_repository.path = 'path'

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
        mocked_repository.path = 'path'

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
        mocked_repository.path = 'path'

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
        mocked_repository.path = 'path'

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

    def user_init(self, *args, **kwargs):
        self.name = args[2]

    @patch('pyolite.models.user.User.__init__', new=user_init)
    def test_user_get_or_create(self):
        mocked_repo = MagicMock()
        mocked_repository = MagicMock()

        mocked_repository.name = 'test_repo'
        mocked_repository.path = 'path'

        with patch.multiple('pyolite.models.lists.users',
                            Repo=MagicMock(return_value=mocked_repo)):
            found_user = object()
            mocked_user_get = MagicMock(return_value=found_user)

            with patch.multiple('pyolite.models.user.User', get=mocked_user_get):
                repo_users = ListUsers(mocked_repository)

                # user found
                user = repo_users.get_or_create('test_user')
                assert user is found_user

                # user created
                mocked_user_get.side_effect = ValueError
                user = repo_users.get_or_create('test_user')
                assert user.name is 'test_user'

    def test_users_set(self):
        mocked_repo = MagicMock()
        mocked_repository = MagicMock()
        mocked_user = MagicMock()

        mock_single_user = MagicMock()
        mock_single_user.name = 'user'

        mocked_repository.name = 'test_repo'
        mocked_repository.path = 'path'

        mocked_user.get.return_value = mock_single_user

        with patch.multiple('pyolite.models.lists.users',
                            Repo=MagicMock(return_value=mocked_repo),
                            User=mocked_user):
            repo_users = ListUsers(mocked_repository)
            repo_users.set((('mocked', 'R'), ('mocked', 'RW+')))

            serialized_users = "repo test_repo\n    R     =    user\n" \
                               "    RW+     =    user\n"
            mocked_repo.overwrite.assert_called_once_with(serialized_users)

            message = "Initialized repository test_repo with users: test, user"
            mocked_repository.git.commit.has_calls([call(['conf'], message)])
