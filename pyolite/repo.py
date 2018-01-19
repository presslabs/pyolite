import re
import fcntl

from .patterns import CONFIG_PATTERN


class Repo(object):
    """
    Low level class, used to operate over raw gitolite config files.
    A gitolite config file has the following structure:

    repo repo_name
        RW    =    readwriteuser
        RW+   =    @readwritegroup
        R     =    readuser

        config gitolite.mirror.simple = "git@github.com:user/repo.git"
    """

    def __init__(self, path):
        self.path = path

    def replace(self, pattern, string):
        with open(str(self.path), 'r+') as f:
            fcntl.flock(f, fcntl.LOCK_EX)

            content = f.read()
            content = re.sub(pattern, string, content)

            f.seek(0)
            f.write(content)
            f.truncate()

            fcntl.flock(f, fcntl.LOCK_UN)

    @property
    def users(self):
        if not self.path.exists():
            return []

        users = []
        with open(str(self.path)) as f:
            fcntl.flock(f, fcntl.LOCK_EX)
            config = f.read()
            fcntl.flock(f, fcntl.LOCK_UN)
            for match in re.compile(r'=( *)(\w+)').finditer(config):
                users.append(match.group(2))

        return users

    def read(self):
        with open(str(self.path)) as f:
            fcntl.flock(f, fcntl.LOCK_EX)
            config = f.read()
            fcntl.flock(f, fcntl.LOCK_UN)

        return config

    def write(self, string):
        with open(self.path, 'a') as f:
            fcntl.flock(f, fcntl.LOCK_EX)
            f.write(string)
            fcntl.flock(f, fcntl.LOCK_UN)

    def overwrite(self, string):
        with open(self.path, 'w') as f:
            fcntl.flock(f, fcntl.LOCK_EX)
            f.write(string)
            fcntl.flock(f, fcntl.LOCK_UN)

    def write_config(self, config):
        """
        Overwrite only the config part of a repository, not the users.
        """

        new_content = ""
        content = self.read()

        for line in content.split("\n"):
            if not re.match(CONFIG_PATTERN, line):
                new_content += line + "\n"

        return self.overwrite(new_content + config)
