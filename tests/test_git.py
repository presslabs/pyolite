from unittest import TestCase

from mock import MagicMock, patch, call
from nose.tools import raises

from pyolite.git import Git


class TestGit(TestCase):
    @raises(ValueError)
    def test_commit_with_no_message(self):
        mock_repo = MagicMock()

        git = Git(mock_repo)
        objects = ['simple_object', 'more_complex_one']

        git.commit(objects, '')

    def test_commit_succesfully_with_multiple_objects(self):
        mock_repo = MagicMock()

        mock_os = MagicMock()
        mock_env = MagicMock()
        mock_os.environ.copy.return_value = mock_env

        mock_git = MagicMock()

        with patch.multiple('pyolite.git', os=mock_os, git=mock_git):
            git = Git(mock_repo)

            objects = ['simple_object', 'more_complex_one']
            commit_message = 'simple commit message'

            git.commit(objects, commit_message)

        mock_os.environ.copy.assert_called_once_with()
        mock_env.update.assert_called_once_with({'GIT_WORK_TREE': mock_repo,
                                                 'GIT_DIR': '%s/.git' % mock_repo})
        mock_git.gc.assert_called_once_with('--force', '--prune', _env=mock_env)
        mock_git.checkout.assert_called_once_with('HEAD', _env=mock_env)
        mock_git.pull("origin", "master", _env=mock_env)

        mock_git.add.assert_has_calls([call('-A', objects[0], _env=mock_env),
                                       call('-A', objects[1], _env=mock_env)])

        mock_git.commit.assert_called_once_with('-m', commit_message, _env=mock_env)
        mock_git.push.assert_called_once_with(_env=mock_env)
