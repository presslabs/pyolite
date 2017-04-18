from unipath import Path

from pyolite.models.lists import ListKeys


class User(object):
    def __init__(self, path, git, name, **kwargs):
        self.name = name
        self.repos = kwargs.get('repos') or []

        self.path = path
        self.git = git

        self.keys = ListKeys(self, kwargs.get('keys') or [])

    @classmethod
    def get_by_name(cls, name, path, git):
        # get user's keys
        key_path = Path(path, 'keydir')
        keys = [key for key in key_path.walk() if
                key.endswith('%s.pub' % name)]

        # get user's repos
        repos = []
        repos_path = Path(path, 'conf/')
        for repo in repos_path.walk():
            if repo.isdir():
                continue

            with open(str(repo)) as f:
                if name in f.read():
                    repos.append(repo)

        if repos or keys:
            return cls(path, git, name, **{'repos': repos, 'keys': keys})

        return None

    @classmethod
    def get(cls, user, path, git):
        if isinstance(user, str):
            user = User.get_by_name(user, path, git)

        if not isinstance(user, User) or not user:
            message = 'Missing user or invalid type'
            raise ValueError(message)

        return user

    @property
    def is_admin(self):
        for repo in self.repos:
            if 'gitolite.conf' in repo:
                return True
        return False

    def __str__(self):
        return "< %s >" % self.name

    def __repr__(self):
        return "< %s >" % self.name
