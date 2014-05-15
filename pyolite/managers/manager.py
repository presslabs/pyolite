from abc import ABCMeta, abstractmethod


class Manager(object):
  __metaclass__ = ABCMeta

  def __init__(self, admin_repository):
    self.admin_repository = admin_repository

  def get_or_create(self, lookup_entity):
    entity = self.get(lookup_entity)

    if not entity:
      entity = self.create(lookup_entity)

    return entity

  @abstractmethod
  def get(self, entity):
    raise NotImplementedError("Each manager has a get method")

  @abstractmethod
  def create(self, entity):
    raise NotImplementedError("Each manager has a create method")
