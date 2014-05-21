import re

from unipath import Path


class ListUsers(object):
  def __init__(self, repo):
    self.repo = repo
    self._users = self._get_users()

  def _get_users(self):
    # TODO: check for groups
    users = []
    repo_config = Path(self.repo.path, 'conf/repos/',
                       "%s.conf" % self.repo.name)

    with open(str(repo_config)) as f:
      config = f.read()
      for match in re.compile('=( *)(\w+)').finditer(config):
        users.append(match.group(2))

    return users

  def append(self, item):
    pass

  def __iter__(self):
    for user in self._user:
      yield user

  def __getitem__(self, item):
    return self._users[item]

  def __setitem__(self, item, value):
    self._users[item] = value

  def __add__(self, items):
    for item in items:
      self.append(item)

  def __str__(self):
    return "['%s']" % ', '.join(self._users)
