class ListUsers(object):
  def __init__(self, repo):
    self.repo = repo
    self._users = []

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

  def append(self, item):
    pass
