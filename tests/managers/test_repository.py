from unittest import TestCase

from mock import MagicMock, patch
from nose.tools import eq_

from pyolite.managers.repository import RepositoryManager


class TestRepositoryManager(TestCase):
  def test_get_repository(self):
    mocked_repository = MagicMock()
    mocked_repository.get_by_name.return_value = 'my_repo'

    mocked_path = MagicMock()
    mocked_git = MagicMock()

    with patch.multiple('pyolite.managers.manager',
                        Path=MagicMock(return_value=mocked_path),
                        Git=MagicMock(return_value=mocked_git)):
      with patch.multiple('pyolite.managers.repository',
                          Repository=mocked_repository):

        repos = RepositoryManager('/path/to/admin/repo/')

        eq_(repos.get('my_repo'), 'my_repo')
        mocked_repository.get_by_name.assert_called_once_with('my_repo',
                                                              mocked_path,
                                                              mocked_git)
