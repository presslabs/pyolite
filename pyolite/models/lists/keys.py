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

        if key in self:
            return

        directory = Path(self.user.path, 'keydir', self.user.name,
                         hashlib.md5(key.strip().split()[1]).hexdigest())
        directory.mkdir(parents=True)

        key_file = Path(directory, "%s.pub" % self.user.name)
        if key_file.exists() and key_file.read_file() == key:
            return

        key_file.write_file(key)

        self.user.git.commit(['keydir'],
                             'Added new key for user %s' % self.user.name)

        super(ListKeys, self).append(key)

    def remove(self, key):
        directory = Path(self.user.path, 'keydir', self.user.name,
                         hashlib.md5(key.strip().split()[1]).hexdigest())
        key_file = Path(directory, "%s.pub" % self.user.name)

        if not key_file.exists():
            raise ValueError("Invalid key")

        key_file.remove()
        key_file.parent.rmdir()

        self.user.git.commit(['keydir'],
                             'Removed key for user %s' % self.user.name)

    def __add__(self, keys):
        for key in keys:
            self.append(key)
