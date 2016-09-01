from abc import ABCMeta, abstractmethod

from unipath import Path

from pyolite.git import Git


class Manager(object):
    __metaclass__ = ABCMeta

    def __init__(self, admin_repository):
        self.path = Path(admin_repository)
        self.git = Git(admin_repository)

        if not self.path.isdir():
            raise ValueError('Admin repository path should point to directory')

    def get_or_create(self, lookup_entity, *args, **kwargs):
        return self.get(lookup_entity) or self.create(lookup_entity, *args,
                                                      **kwargs)

    @abstractmethod
    def get(self, entity):
        raise NotImplementedError("Each manager needs a get method")

    @abstractmethod
    def create(self, entity):
        raise NotImplementedError("Each manager needs a create method")
