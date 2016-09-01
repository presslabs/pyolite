from unittest import TestCase

from mock import MagicMock, patch
from nose.tools import eq_

from pyolite import Pyolite


class TestPyolite(TestCase):
    def test_if_pyolite_object_has_all_attributes(self):
        mocked_repository = MagicMock()
        mocked_user = MagicMock()

        with patch.multiple('pyolite.pyolite',
                            RepositoryManager=mocked_repository,
                            UserManager=mocked_user):
            pyolite = Pyolite('my_repo')

            eq_(pyolite.admin_repository, 'my_repo')
            mocked_repository.assert_called_once_with('my_repo')
            mocked_user.assert_called_once_with('my_repo')
