from pyolite import Pyolite

# initial olite object
admin_repository = '/home/wok/presslabs/pyolite/gitolite-admin/'
olite = Pyolite(admin_repository=admin_repository)

# create user object
vlad = olite.users.create(name='ameno',
                          key_path='/home/wok/.ssh/second_rsa.pub')

# get user by name
vlad = olite.users.get(name='ameno')

# get_or_create django style
vlad = olite.users.get_or_create('ameno')

# check if user is admin or not
print vlad.is_admin

# TODO:
# vlad.repos['oxygen'].permissions = 'RW+'
