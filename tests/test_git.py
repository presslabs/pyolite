from unittest import TestCase

from mock import MagicMock, patch
from nose.tools import raises, eq_

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

  def test_commit_succesfully_with_multiple_objects(self):
    mock_repo = MagicMock()
    mock_index = MagicMock()
    mock_remotes = MagicMock()

    mock_repo.index = mock_index
    mock_repo.remotes.origin = mock_remotes

    with patch.multiple('pyolite.git', Repo=MagicMock(return_value=mock_repo)):
      git = Git('~/path/to/repo')

      objects = ['simple_object', 'more_complex_one']
      commit_message = 'simple commit message'

      git.commit(objects, commit_message)

    mock_index.add.assert_called_once_with(objects)
    mock_index.commit.assert_called_once_with(commit_message)

    eq_(mock_remotes.fetch.call_count, 1)
    eq_(mock_remotes.pull.call_count, 1)
    eq_(mock_remotes.push.call_count, 1)
