class Repository(object):
  def __init__(self, name):
    self.name = name

  def add_user(self, name, raw_key=None, path_key=None):
    pass

  @property
  def users(self):
    pass

  def remove_user(name):
    pass

  def save(self):
    # git commit; git push
    pass
