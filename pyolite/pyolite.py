from managers.repository import RepositoryManager
from managers.user import UserManager


class Pyolite(object):
    def __init__(self, admin_repository):
        self.admin_repository = admin_repository

        self.users = UserManager(admin_repository)
        self.repos = RepositoryManager(admin_repository)
