import hashlib

from unipath import Path

from pyolite.models.user import User
from .manager import Manager


class UserManager(Manager):
  def get(self, user):
    pass

  def create(self, name, key=None, key_path=None):
    if key is None and key_path is None:
      raise ValueError('You need to specify a key or key_path')

    if key_path:
      with open(key_path) as f:
        key = f.read()

    directory = Path(self.path, 'keydir', hashlib.md5(key).hexdigest())
    directory.mkdir()

    key_file = Path(directory, "%s.pub" % name)
    key_file.write_file(key)

    self.git.commit(['keydir'], 'Added new key for user %s' % name)
    return User.get_by_name(name, self.path)
