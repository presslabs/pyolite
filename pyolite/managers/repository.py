from unipath import Path

from pyolite.models.repository import Repository
from pyolite.managers.manager import Manager


class RepositoryManager(Manager):
    def get(self, entity):
        return Repository.get_by_name(entity, self.path, self.git)

    def create(self, entity):
        repo_file = Path(self.path, 'conf/repos/%s.conf' % entity)
        if repo_file.exists():
            raise ValueError('Repository %s already exists' % entity)
        # If there are missing parent paths in the repo path, create them so we don't get IOErrors
        # In the case of a repo having names with slashes (e.g. "username/reponame")
        elif repo_file.parent != Path(""):
            repo_file.parent.mkdir(parents=True)

        repo_file.write_file("repo %s\n" % entity)

        self.git.commit([str(repo_file)], 'Created repo %s' % entity)

        return Repository(entity, self.path, self.git)
