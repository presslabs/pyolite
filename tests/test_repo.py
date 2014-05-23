from unittest import TestCase

from mock import MagicMock, patch
from nose.tools import eq_

from pyolite.repo import Repo


class TestRepo(TestCase):
  def test_it_should_replace_a_given_string_in_repo_conf(self):
    mocked_path = MagicMock()
    mocked_re = MagicMock()

    mocked_path = 'tests/fixtures/config.conf'
    mocked_re.sub.return_value = 'another_text'

    with patch.multiple('pyolite.repo', re=mocked_re):
      repo = Repo(mocked_path)
      repo.replace('pattern', 'string')

      with open('tests/fixtures/config.conf') as f:
        eq_(f.read(), 'another_text')

      mocked_re.sub.assert_called_once_with('pattern', 'string',
                                            'another_text')

  def test_it_should_retrieve_all_users_from_repo(self):
    mocked_path = MagicMock()
    mocked_re = MagicMock()
    mocked_user1 = MagicMock()
    mocked_user2 = MagicMock()

    mocked_path = 'tests/fixtures/repo_users.conf'
    mocked_re.compile('=( *)(\w+)').finditer.return_value = [mocked_user1,
                                                             mocked_user2]
    mocked_user1.group.return_value = 'user1'
    mocked_user2.group.return_value = 'user2'

    with patch.multiple('pyolite.repo', re=mocked_re):
      repo = Repo(mocked_path)
      eq_(repo.users, ['user1', 'users'])
