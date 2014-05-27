import Path

from pyolite.repo import Repo
from pyolite.models.user import User


ACCEPTED_PERMISSIONS = set('RW+CD')


class ListUsers(object):
  def __init__(self, repository):
    self.repository_model = repository
    self.repo = Repo(Path(repository.path,
                          "conf/repos/%s.conf" % repository.name))

  def with_user(func):
    def decorated(self, user, *args, **kwargs):
      user = User.get(user, self.repository_model.path,
                      self.repository_model.git)
      return func(self, user, *args, **kwargs)
    return decorated

  @with_user
  def add(self, user, permission):
    if user.name in self.repo.users:
      raise ValueError('User %s already exists. Please check '
                       'example/repository.py in order to see how you can '
                       'delete or change permissions' % user.name)

    if set(map(lambda permission: permission.upper(), permission)) - \
       ACCEPTED_PERMISSIONS != set([]):
      raise ValueError('Invalid permissions. They must be from %s' %
                       ACCEPTED_PERMISSIONS)

    self.repo.write("    %s     =    %s\n" % (permission, user.name))

    commit_message = 'User %s added to repo %s with permissions: %s' %\
                     (user, self.repository_model.name, permission)
    self.repository_model.git.commit(['conf'], commit_message)

    user.repos.append(self.repo)
    return user

  @with_user
  def edit(self, user, permission):
    pattern = r'(\s*)([RW+DC]*)(\s*)=(\s*)%s' % user.name
    string = r"\n    %s    =    %s" % (permission, user.name)

    self.repo.replace(pattern, string)

    self.repo.git.commit(['conf'],
                         "User %s has %s permission for repository %s" %
                         (user.name, permission, self.repo.name))
    return user

  @with_user
  def remove(self, user):
    pattern = r'(\s*)([RW+DC]*)(\s*)=(\s*)%s' % user.name
    self.repo.replace(pattern, "")

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
