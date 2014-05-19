from unittest import TestCase

from mock import MagicMock, patch
from nose.tools import raises

from pyolite.managers.user import UserManager


class TestUser(TestCase):
  @raises(ValueError)
  def test_create_user_with_no_key(self):
    with patch.multiple('pyolite.managers.manager',
                        Git=MagicMock(),
                        Path=MagicMock()):
      users = UserManager('~/path/to/admin/gitolite/repo')
      users.create('test_username')
