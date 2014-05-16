from pyolite.models.repository import Repository
from .manager import Manager


class RepositoryManager(Manager):
  def get(self, lookup_repo):
    return Repository.get_by_name(lookup_repo)

  def create(self, lookup_repo):
    pass

  def get_or_create(self, lookup_repo):
    pass
