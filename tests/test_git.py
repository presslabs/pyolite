from unittest import TestCase

from mock import MagicMock, patch
from nose.tools import raises

from pyolite.git import Git


class TestGit(TestCase):

  @raises(ValueError)
  def test_commit_with_no_message(self):
    mock_repo = MagicMock()
    mock_index = MagicMock()
    mock_remotes = MagicMock()

    mock_repo.index = mock_index
    mock_repo.remotes.origin = mock_remotes

    with patch.multiple('pyolite.git', Repo=mock_repo):
      git = Git('~/path/to/repo')
      objects = ['simple_object', 'more_complex_one']

      git.commit(objects, '')
