from unittest import TestCase

from mock import MagicMock, patch
from nose.tools import eq_

from pyolite.repo import Repo


class TestRepo(TestCase):
  def test_it_should_repalce_a_give_string_in_repo_conf(self):
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
