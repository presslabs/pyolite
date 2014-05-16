from unipath import Path


class User(object):
  def __init__(self, name, repos=None, keys=None):
    self.name = name
    self.repos = repos or []
    self.keys = keys or []

  @classmethod
  def get_by_name(cls, name, admin_path):

    # get user's keys
    key_path = Path(admin_path, 'keydir')
    keys = [key for key in key_path.walk() if key.endswith('%s.pub' % name)]

    # get user's repos
    repos = []
    repos_path = Path(admin_path, 'conf/repos/')
    for repo in repos_path.walk():
      with open(repo) as f:
        if name in f.read():
          repos.append(repo)

    return cls(name, repos, keys)
