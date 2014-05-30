from pyolite import Pyolite

# initial olite object
admin_repository = '/home/absolute/path/to/gitolite/repo/'
olite = Pyolite(admin_repository=admin_repository)

# create user object
vlad = olite.users.create(name='bob',
                          key_path='~/.ssh/second_rsa.pub')

# get user by name
vlad = olite.users.get(name='admin')

# get_or_create django style
vlad = olite.users.get_or_create('alice')

# add new key to user
vlad.keys.append('/path/to/key')
vlad.keys.append('just put the key here')

vlad.keys.remove("my awesome key")

# check if user is admin or not
print vlad.is_admin

# TODO:
# vlad.repos['oxygen'].permissions = 'RW+'
