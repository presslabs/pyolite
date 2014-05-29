import re


class Repo(object):
  def __init__(self, path):
    self.path = path

  def replace(self, pattern, string):
    with open(str(self.path), 'r+') as f:
      content = f.read()
      content = re.sub(pattern, string, content)
      f.seek(0)
      f.write(content)
      f.truncate()

  @property
  def users(self):
    if not self.path.exists():
      return []

    users = []
    with open(str(self.path)) as f:
      config = f.read()
      for match in re.compile('=( *)(\w+)').finditer(config):
        users.append(match.group(2))

    return users

  def write(self, string):
    with open(self.path, 'a') as f:
      f.write(string)
