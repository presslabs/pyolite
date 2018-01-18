import pytest
from mock import MagicMock


@pytest.fixture(autouse=True)
def patch_git(monkeypatch):
    monkeypatch.setattr('pyolite.git.git', MagicMock())
