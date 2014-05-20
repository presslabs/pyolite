from unipath import Path

from pyolite.models.repository import Repository
from .manager import Manager


class RepositoryManager(Manager):
  def __init__(self, *args, **kwargs):
    super(RepositoryManager, self).__init__(*args, **kwargs)
    self.users = self._get_users()

  def get(self, lookup_repo):
    return Repository.get_by_name(lookup_repo, self.path, self.git)

  def create(self, lookup_repo):
    repo_file = Path(self.path, 'conf/repos/%s.conf' % lookup_repo)
    if repo_file.exists():
      raise ValueError('Repository %s already exists' % lookup_repo)

    repo_file.write_file("repo %s\n")

    self.commit([repo_file], 'Created repo %s' % lookup_repo)

    return Repository(lookup_repo, self.path, self.git)

  def get_or_create(self, lookup_repo):
    pass
