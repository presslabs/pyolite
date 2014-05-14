from .repository import Repository


class Pyolite(object):
  def __init__(self, admin_repository):
    self.admin_repository = admin_repository

  def repo(self, name):
    repository = Repository(name)
    repository.save()
    return repository
