from unittest import TestCase

from mock import MagicMock, patch
from nose.tools import raises, eq_

from pyolite.managers.manager import Manager


class TestManager(TestCase):
    @raises(ValueError)
    def test_if_admin_repository_is_not_dir_it_should_raise_ValueError(self):
        mocked_path = MagicMock()
        mocked_git = MagicMock()

        mocked_path.isdir.return_value = False

        with patch.multiple('pyolite.managers.manager',
                            Path=MagicMock(return_value=mocked_path),
                            Git=MagicMock(return_value=mocked_git)):
            with patch.multiple('pyolite.managers.manager.Manager',
                                __abstractmethods__=set()):
                Manager('/path/to/repo')

    def test_get_or_create_method(self):
        mocked_path = MagicMock()
        mocked_git = MagicMock()

        mocked_get = MagicMock(return_value='user')
        mocked_create = MagicMock()

        Manager.get = mocked_get
        Manager.create = mocked_create

        with patch.multiple('pyolite.managers.manager',
                            Path=MagicMock(return_value=mocked_path),
                            Git=MagicMock(return_value=mocked_git)):
            with patch.multiple('pyolite.managers.manager.Manager',
                                __abstractmethods__=set()):
                manager = Manager('/path/to/admin/repo')

                eq_(manager.get_or_create('mine', 'key'), 'user')
                mocked_get.assert_called_once_with('mine')

    @raises(NotImplementedError)
    def test_get_abstract_method_method(self):
        mocked_path = MagicMock()
        mocked_git = MagicMock()

        with patch.multiple('pyolite.managers.manager',
                            Path=MagicMock(return_value=mocked_path),
                            Git=MagicMock(return_value=mocked_git)):
            with patch.multiple('pyolite.managers.manager.Manager',
                                __abstractmethods__=set()):
                manager = Manager('/path/to/admin/repo')
                manager.get('entity')

    @raises(NotImplementedError)
    def test_create_abstract_method_method(self):
        mocked_path = MagicMock()
        mocked_git = MagicMock()

        with patch.multiple('pyolite.managers.manager',
                            Path=MagicMock(return_value=mocked_path),
                            Git=MagicMock(return_value=mocked_git)):
            with patch.multiple('pyolite.managers.manager.Manager',
                                __abstractmethods__=set()):
                manager = Manager('/path/to/admin/repo')
                manager.create('entity')
