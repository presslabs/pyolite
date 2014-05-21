import re

from unipath import Path

from pyolite.models.user import User


class ListUsers(object):
  def __init__(self, repo):
    self.repo = repo
    self.repo_config = Path(self.repo.path, 'conf/repos/',
                            "%s.conf" % self.repo.name)

    self._users = self._get_users()

  def _get_users(self):
    # TODO: check for groups
    users = []

    with open(str(self.repo_config)) as f:
      config = f.read()
      for match in re.compile('=( *)(\w+)').finditer(config):
        users.append(match.group(2))

    return users

  def add(self, user, permission):
    if not isinstance(user, User):
      message = 'We need an user object. Please see examples/repository'
      raise ValueError(message)

    with open(str(self.repo_config)) as f:
      # check if we have the user in repo
      users = re.compile('=( *)(\w+)').findall(f.read())
      print users

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
