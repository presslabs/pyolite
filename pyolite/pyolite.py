from .repository import Repository


class Pyolite(object):
  def __init__(self, repository):
    self.repository = repository

  def repo(self, name):
    repository = Repository(name)
    repository.save()
    return repository
