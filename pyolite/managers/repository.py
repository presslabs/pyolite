import re
from unipath import Path

from models.repository import Repository
from .manager import Manager


class RepositoryManager(Manager):
  def __init__(self, *args, **kwargs):
    super(RepositoryManager, self).__init__(*args, **kwargs)

  def get(self, lookup_repo):
    return Repository.get_by_name(lookup_repo, self.path, self.git)

  def create(self, lookup_repo):
    repo_file = Path(self.path, 'conf/repos/%s.conf' % lookup_repo)
    if repo_file.exists():
      raise ValueError('Repository %s already exists' % lookup_repo)
    # If there are missing parent paths in the repo path, create them so we don't get IOErrors
    # In the case of a repo having names with slashes (e.g. "username/reponame")
    elif repo_file.parent != Path(""):
      repo_file.parent.mkdir(parents=True)

    repo_file.write_file("repo %s\n" % lookup_repo)

    self.git.commit([str(repo_file)], 'Created repo %s' % lookup_repo)

    return Repository(lookup_repo, self.path, self.git)

  def delete(self, lookup_repo_name):
    repo = Repository(lookup_repo_name, self.path, self.git)
    dest = Path(self.path, 'conf/repos/%s.conf' % lookup_repo_name)
    if not dest.exists():
      raise ValueError('Repository %s not existing.' % lookup_repo_name)
    dest.remove()
    self.git.commit([str(dest)], 'Deleted repo %s.' % lookup_repo_name)

    return repo

  def all(self):
    repos = []
    repo_dir = Path(self.path, 'conf/repos')

    for obj in repo_dir.walk():
      if obj.isdir():
        continue

      files = re.compile('(\w+.conf$)').findall(str(obj))
      if files:
        repos += files

    return [Repository.get_by_name(repo[:-5], self.path, self.git)
            for repo in set(repos)]