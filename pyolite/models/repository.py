from unipath import Path


class Repository(object):
  def __init__(self, name, path, git):
    self.name = name
    self.path = path
    self.git = git

  @classmethod
  def get_by_name(cls, lookup_repo, path, git):
    for obj in Path(path, 'conf').walk():
      if obj.isdir():
        continue

      with open(obj) as f:
        if "repo %s" % lookup_repo in f.read():
          return cls(lookup_repo, path, git)
    return None
