from __future__ import absolute_import

from git import Repo


class Git(object):
  def __init__(self, repo, remote='origin'):
    self.repo = Repo(repo)
    self.index = self.repo.index
    self.remote = getattr(self.repo.remotes, remote)

  def commit(self, objects, message, action='add'):
    # validate commit message
    if not message or not isinstance(message, basestring):
      raise ValueError("Commit message should not be empty or not string")

    # create the commit
    if action == 'add':
      self.index.add(objects)

    if action == 'remove':
      self.index.remove(objects)

    self.index.commit(message)

    # fetch, pull and push from and to the remote
    self.remote.fetch()
    self.remote.pull()
    self.remote.push()
