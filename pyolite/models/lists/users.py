from unipath import Path

from pyolite.models.user import User
from pyolite.repo import Repo

ACCEPTED_PERMISSIONS = set('RW+CD')


class ListUsers(object):
    def __init__(self, repository):
        self.repository_model = repository
        self.repo = Repo(Path(repository.path,
                              "conf/repos/%s.conf" % repository.name))

    def with_user(func):
        def decorated(self, string_user, *args, **kwargs):
            try:
                user = User.get(string_user, self.repository_model.path,
                                self.repository_model.git)
            except ValueError:
                user = User(self.repository_model.path,
                            self.repository_model.git,
                            string_user)
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

        commit_message = 'User %s added to repo %s with permissions: %s' % \
                         (user, self.repository_model.name, permission)
        self.repository_model.git.commit(['conf'], commit_message)

        user.repos.append(self.repo)
        return user

    @with_user
    def edit(self, user, permission):
        pattern = r'(\s*)([RW+DC]*)(\s*)=(\s*)%s' % user.name
        string = r"\n    %s    =    %s" % (permission, user.name)

        self.repo.replace(pattern, string)

        self.repository_model.git.commit(['conf'],
                                         "User %s has %s permission for repository %s" %
                                         (user.name, permission,
                                          self.repository_model.name))
        return user

    @with_user
    def remove(self, user):
        pattern = r'(\s*)([RW+DC]*)(\s*)=(\s*)%s' % user.name
        self.repo.replace(pattern, "")

        self.repository_model.git.commit(['conf'],
                                         "Deleted user %s from repository %s" %
                                         (user.name,
                                          self.repository_model.name))

    @with_user
    def get_or_create(self, user):
        return user

    def set(self, users=None):
        users_serialized = "repo {}\n".format(self.repository_model.name)
        if isinstance(users, dict):
            users = users.iteritems()

        if users:
            for user, permission in users:
                if not hasattr(user, 'name'):
                    user = self.get_or_create(user)

                users_serialized += "    %s     =    %s\n" % (permission,
                                                              user.name)

        self.repo.overwrite(users_serialized)

        users = ", ".join((user for user, permission in users))
        commit_message = "Initialized repository %s with users: %s" % (
            self.repository_model.name, users
        )
        self.repository_model.git.commit(['conf'], commit_message)

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
        return "['%s']" % ', '.join(self.repo.users)
