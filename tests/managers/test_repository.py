import pytest
from mock import MagicMock, patch, call

from pyolite.managers.repository import RepositoryManager

from tests.mocked_manager import MockManager, mocked_git, mocked_path


def test_get_repository():
    mocked_repository = MagicMock()
    mocked_repository.get_by_name.return_value = 'my_repo'

    RepositoryManager.__bases__ = (MockManager,)
    with patch.multiple('pyolite.managers.repository',
                        Repository=mocked_repository):
        repos = RepositoryManager('/path/to/admin/repo/')

        assert repos.get('my_repo') == 'my_repo'
        mocked_repository.get_by_name.assert_called_once_with('my_repo',
                                                              mocked_path,
                                                              mocked_git)

def test_create_new_repository_that_already_exists():
    mocked_repository = MagicMock()

    mocked_file = MagicMock()

    mocked_path.return_value = mocked_file
    mocked_file.exists.return_value = True

    RepositoryManager.__bases__ = (MockManager,)
    with patch.multiple('pyolite.managers.repository',
                        Path=mocked_path,
                        Repository=mocked_repository):
        with pytest.raises(ValueError):
            repos = RepositoryManager('/path/to/admin/repo/')
            repos.create('already_exists')

def test_it_should_commit_if_a_new_repository_was_succesfully_created():
    mocked_repository = MagicMock()

    mocked_file = MagicMock()
    mocked_file.__str__ = lambda x: 'dont_exists'

    mocked_file.exists.return_value = False
    mocked_path.return_value = mocked_file

    mocked_repository.return_value = 'new repo'

    RepositoryManager.__bases__ = (MockManager,)

    with patch.multiple('pyolite.managers.repository',
                        Path=mocked_path,
                        Repository=mocked_repository):
        repos = RepositoryManager('/path/to/admin/repo/')
        repo = repos.create('dont_exists')

        mocked_path.has_calls(call(mocked_path,
                                   'conf/repos/dont_exists.conf'))
        assert mocked_file.exists.call_count == 1
        mocked_file.write_file.assert_called_once_with(
            'repo dont_exists\n')
        mocked_git.commit.has_calls(call(['dont_exists'],
                                         'Created repo dont_exists'))
        mocked_repository.assert_called_once_with('dont_exists',
                                                  mocked_path,
                                                  mocked_git)
        assert repo == 'new repo'
