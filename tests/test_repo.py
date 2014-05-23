from unittest import TestCase

from mock import MagicMock, patch
from nose.tools import eq_

from pyolite.repo import Repo


class TestRepo(TestCase):
  def test_it_should_replace_a_given_string_in_repo_conf(self):
    mocked_re = MagicMock()
    path = 'tests/fixtures/config.conf'

    mocked_re.sub.return_value = 'another_text'

    with patch.multiple('pyolite.repo', re=mocked_re):
      repo = Repo(path)
      repo.replace('pattern', 'string')

      with open('tests/fixtures/config.conf') as f:
        eq_(f.read(), 'another_text')

      mocked_re.sub.assert_called_once_with('pattern', 'string',
                                            'another_text')

  def test_it_should_retrieve_all_users_from_repo(self):
    path = 'tests/fixtures/repo_users.conf'

    mocked_re = MagicMock()
    mocked_user1 = MagicMock()
    mocked_user2 = MagicMock()

    mocked_re.compile('=( *)(\w+)').finditer.return_value = [mocked_user1,
                                                             mocked_user2]
    mocked_user1.group.return_value = 'user1'
    mocked_user2.group.return_value = 'user2'

    with patch.multiple('pyolite.repo', re=mocked_re):
      repo = Repo(path)
      eq_(repo.users, ['user1', 'user2'])

  def test_it_shoujld_write_to_repo_config(self):
    path = 'tests/fixtures/empty_repo.conf'

    Repo(path).write('some_text')

    with open(path, 'r+') as f:
      eq_('some_text', f.read())

      f.seek(0)
      f.write('')
      f.truncate()
