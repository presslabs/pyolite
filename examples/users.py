from pyolite import Pyolite

# initial olite object
admin_repository = 'gitolite-admin/'
olite = Pyolite(admin_repository=admin_repository)

# create user object
vlad = olite.users.create(name='vlad', key_path='/home/wok/.ssh/id_rsa.pub')

# get user by name
vlad = olite.users.get(name='vlad')

# get_or_create django style
vlad = olite.users.get_or_create(name='vlad')

# check if user is admin or not
print vlad.is_admin
