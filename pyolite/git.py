from __future__ import absolute_import
import os

from sh import git


class Git(object):
  def __init__(self, repo):
    self.repo = repo

  def commit(self, objects, message):
    # validate commit message
    if not message or not isinstance(message, basestring):
      raise ValueError("Commit message should not be empty or not string")

    os.chdir(self.repo)

    # pull and push from and to the remote
    git.pull()

    for obj in objects:
      git.add("-A", obj)

    git.commit("-m", message)

    git.push()
