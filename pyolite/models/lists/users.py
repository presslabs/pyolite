import re

from unipath import Path

from pyolite.models.user import User


ACCEPTED_PERMISSIONS = set('RW+CD')


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

    # TODO: return a users manager
    return users

  def _get_user(self, user):
    if isinstance(user, basestring):
      user = User.get_by_name(user, self.repo.path, self.repo.git)

    if not isinstance(user, User) or not user:
      message = 'We need an user object. Please see examples/repository'
      raise ValueError(message)

    return user

  def _replace_in_repo(self, pattern, string):
    with open(str(self.repo_config), 'r+') as f:
      content = f.read()
      content = re.sub(pattern, string, content)
      f.seek(0)
      f.write(content)
      f.truncate()

  def add(self, user, permission):
    user = self._get_user(user)

    with open(str(self.repo_config), 'a+') as f:
      # check if we have the user in repo
      users = [item[1] for item in re.compile('=( *)(\w+)').findall(f.read())]
      if user.name in users:
        raise ValueError('User %s already exists. Please check '
                         'example/repository.py in order to see how you can '
                         'delete or change permissions' % user.name)

      # check user's permissions
      if set(map(lambda permission: permission.upper(), permission)) - \
         ACCEPTED_PERMISSIONS != set([]):
        raise ValueError('Invalid permissions. They must be from %s' %
                         ACCEPTED_PERMISSIONS)
      # add user to repo
      f.write("    %s     =    %s\n" % (permission, user.name))
      self.repo.git.commit(['conf'],
                           'User %s added to repo %s with permissions: %s' %
                           (user, self.repo.name, permission))

    user.repos.append(self.repo)
    return user

  def edit(self, user, permission):
    user = self._get_user(user)

    pattern = r'(\s*)([RW+DC]*)(\s*)=(\s*)%s' % user.name
    string = r"\n    %s    =    %s" % (permission, user.name)

    self._replace_in_repo(pattern, string)

    self.repo.git.commit(['conf'],
                         "User %s has %s permission for repository %s" %
                         (user.name, permission, self.repo.name))
    return user

  def remove(self, user):
    user = self._get_user(user)

    pattern = r'(\s*)([RW+DC]*)(\s*)=(\s*)%s' % user.name
    self._replace_in_repo(pattern, "")

    self.repo.git.commit(['conf'],
                         "Deleted user %s from repository %s" %
                         (user.name, self.repo.name))

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
