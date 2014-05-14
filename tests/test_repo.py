from unittest import TestCase

from mock import MagicMock, patch
from nose.tools import eq_

from pyolite import Pyolite


class TestRepo(TestCase):
  def test_create_repo_with_no_user(self):
    mock_repository = MagicMock()
    mock_repo = MagicMock()

    mock_repository.return_value = mock_repo
    admin_repo = 'tests/fixtures/admin-repo'

    with patch.multiple('pyolite.pyolite', Repository=mock_repository):
      olite = Pyolite(admin_repo)

      eq_(olite.repo(admin_repo), mock_repo)
      eq_(mock_repo.save.call_count, 1)
