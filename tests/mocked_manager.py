from mock import MagicMock

mocked_git = MagicMock()
mocked_path = MagicMock()

MockManager = MagicMock
MockManager.git = mocked_git
MockManager.path = mocked_path
