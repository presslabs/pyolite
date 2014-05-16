from pyolite.models.user import User
from .manager import Manager


class UserManager(Manager):
  def create(self, name, key=None, key_path=None):
    if key is None and key_path is None:
      raise ValueError('You need to specify a key or key_path')

    user = User(self.path, self.git, name, keys=[key or key_path])
    print user

  def get(self, name):
    return User.get_by_name(name, self.path, self.git)
