from __future__ import absolute_import

from git import Repo


class Git(object):
  def __init__(self, repo, remote='origin'):
    self.repo = Repo(repo)
    self.index = self.repo.index
    self.remote = getattr(self.repo.remotes, remote)

  def commit(self, objects, message):
    self.index.add(objects)

    self.index.commit(message)

    # fetch, pull and push from and to the remote
    self.remote.fetch()
    self.remote.pull()
    self.remote.push()
