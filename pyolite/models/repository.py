from unipath import Path

from git import Repo


class Repository(object):
  def __init__(self, name, path, git):
    self.name = name
    self.path = path
    self.git = git

  @classmethod
  def get_by_name(cls, lookup_repo, admin_path):
    for obj in Path(admin_path, 'conf'):
      if obj.isdir():
        continue

      with open(obj) as f:
        if "repo %s" % lookup_repo in f.read():
          return cls(lookup_repo, Path(admin_path), Repo(admin_path))
