import re

from unipath import Path

from pyolite.models.user import User
from pyolite.managers.manager import Manager


class UserManager(Manager):
  def create(self, name, key=None, key_path=None):
    if key is None and key_path is None:
      raise ValueError('You need to specify a key or key_path')

    return User(self.path, self.git, name, keys=[key or key_path])

  def get(self, name):
    return User.get_by_name(name, self.path, self.git)

  def all(self):
    users = []
    key_dir = Path(self.path, 'keydir')

    for obj in key_dir.walk():
      if obj.isdir():
        continue

      files = re.compile('(\w+.pub)').findall(str(obj))
      if files:
        users += files

    return [User.get_by_name(user[:-4], self.path, self.git)
            for user in set(users)]
