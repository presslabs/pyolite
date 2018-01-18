import pytest
from mock import MagicMock, patch, call

from pyolite.managers.user import UserManager
from tests.mocked_manager import MockManager, mocked_git, mocked_path


def test_create_user_with_no_key():
    with patch.multiple('pyolite.managers.manager',
                        Git=MagicMock(),
                        Path=MagicMock()):
        with pytest.raises(ValueError):
            users = UserManager('~/path/to/admin/gitolite/repo')
            users.create('test_username')

def test_create_user_succesfully():
    mocked_user_obj = MagicMock()
    mocked_user = MagicMock(return_value=mocked_user_obj)

    UserManager.__bases__ = (MockManager,)
    with patch.multiple('pyolite.managers.user', User=mocked_user,
                        Manager=MagicMock()):
        users = UserManager('~/path/to/admin/gitolite/repo')

        assert mocked_user_obj == users.create('test_username', 'key_path')
        mocked_user.assert_called_once_with(mocked_path, mocked_git,
                                            'test_username')
        mocked_user_obj.keys.append.assert_called_once_with('key_path')

def test_get_user():
    mocked_user = MagicMock()
    mocked_user.get_by_name.return_value = 'test_user'

    UserManager.__bases__ = (MockManager,)
    with patch.multiple('pyolite.managers.user', User=mocked_user):
        users = UserManager('~/path/to/admin/gitolite/repo')

        assert users.get('test_user') == 'test_user'
        mocked_user.get_by_name.assert_called_once_with('test_user',
                                                        mocked_path, mocked_git)

def test_get_all_users():
    mocked_key_dir = MagicMock()
    mocked_file = MagicMock()
    mocked_dir = MagicMock()
    mocked_re = MagicMock()

    mocked_user = MagicMock()
    mocked_user.get_by_name.return_value = 'test_user'

    mocked_path.return_value = mocked_key_dir
    mocked_dir.isdir.return_value = True
    mocked_file.isdir.return_value = False
    mocked_file.__str__ = lambda x: 'ok_file'

    mocked_re.compile().findall.return_value = ['file1.pub']

    mocked_key_dir.walk.return_value = [mocked_file, mocked_dir]

    UserManager.__bases__ = (MockManager,)
    with patch.multiple('pyolite.managers.user', User=mocked_user,
                        Path=mocked_path, re=mocked_re):
        users = UserManager('~/path/to/admin/gitolite/repo')

        assert users.all() == ['test_user']
        mocked_path.has_calls([call(mocked_path, 'keydir')])
        assert mocked_key_dir.walk.call_count == 1
        assert mocked_dir.isdir.call_count == 1
        assert mocked_file.isdir.call_count == 1

        mocked_re.compile.has_calls([call(r'(\w.pub)')])
        mocked_re.compile(r'\w.pub').findall.assert_called_once_with(r'ok_file')

        mocked_user.get_by_name.assert_called_once_with('file1', mocked_path, mocked_git)
