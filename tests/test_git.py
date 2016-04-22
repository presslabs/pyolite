from unittest import TestCase

from mock import MagicMock, patch, call
from nose.tools import raises, eq_

from git import Git


class TestGit(TestCase):

  @raises(ValueError)
  def test_commit_with_no_message(self):
    mock_repo = MagicMock()
    mock_index = MagicMock()
    mock_remotes = MagicMock()

    mock_repo.index = mock_index
    mock_repo.remotes.origin = mock_remotes

    with patch.multiple('git', Repo=mock_repo):
      git = Git('~/path/to/repo')
      objects = ['simple_object', 'more_complex_one']

      git.commit(objects, '')

  def test_commit_succesfully_with_multiple_objects(self):
    mock_repo = MagicMock()
    mock_index = MagicMock()
    mock_remotes = MagicMock()

    mock_repo.index = mock_index
    mock_repo.remotes.origin = mock_remotes

    with patch.multiple('git', Repo=MagicMock(return_value=mock_repo)):
      git = Git('~/path/to/repo')

      objects = ['simple_object', 'more_complex_one']
      commit_message = 'simple commit message'

      git.commit(objects, commit_message)
      git.commit(objects, commit_message, action='remove')

    mock_index.add.assert_called_once_with(objects)
    mock_index.remove.assert_called_once_with(objects)
    mock_index.commit.has_calls([call(commit_message), call(commit_message)])

    eq_(mock_remotes.fetch.call_count, 2)
    eq_(mock_remotes.pull.call_count, 2)
    eq_(mock_remotes.push.call_count, 2)
