from mock import MagicMock

from pyolite.models.lists.users import ListUsers


mocked_repository = MagicMock()
mocked_path = MagicMock()

mocked_users = MagicMock(spec=ListUsers)
mocked_users._get_users = lambda x: []

mocked_users.repo = mocked_repository
mocked_users.repo_config = ''
