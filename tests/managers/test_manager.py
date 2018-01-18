import pytest
from mock import MagicMock, patch

from pyolite.managers.manager import Manager


def test_if_admin_repository_is_not_dir_it_should_raise_ValueError():
    mocked_path = MagicMock()
    mocked_git = MagicMock()

    mocked_path.isdir.return_value = False

    with patch.multiple('pyolite.managers.manager',
                        Path=MagicMock(return_value=mocked_path),
                        Git=MagicMock(return_value=mocked_git)):
        with patch.multiple('pyolite.managers.manager.Manager',
                            __abstractmethods__=set()):
            with pytest.raises(ValueError):
                Manager('/path/to/repo')


def test_get_or_create_method():
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

            assert manager.get_or_create('mine', 'key') == 'user'
            mocked_get.assert_called_once_with('mine')
