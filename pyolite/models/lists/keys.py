import hashlib

from unipath import Path


class ListKeys(list):
  def __init__(self, user, *args, **kwargs):
    super(ListKeys, self).__init__(*args, **kwargs)
    self.user = user

  def append(self, key):
    key_path = Path(key)

    if key_path.isfile():
      with open(str(key_path)) as f:
        key = f.read()

    directory = Path(self.user.path, 'keydir', hashlib.md5(key).hexdigest())
    directory.mkdir()

    key_file = Path(directory, "%s.pub" % self.user.name)
    key_file.write_file(key)

    self.user.git.commit(['keydir'],
                         'Added new key for user %s' % self.user.name)

    super(ListKeys, self).append(key)

  def remove(self, key):
    directory = Path(self.user.path, 'keydir', hashlib.md5(key).hexdigest())
    key_file = Path(directory, "%s.pub" % self.user.name)

    if not key_file.exists():
      raise ValueError("Invalid key")

    try:
      key_file.remove()
    except OSError:
      return False

    self.user.git.commit([str(key_file)],
                         'Removed key for user %s' % self.user.name,
                         action='remove')
    return True

  def __add__(self, keys):
    for key in keys:
      self.append(key)
