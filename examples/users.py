from pyolite import Pyolite

# initial olite object
admin_repository = 'gitolite-admin/'
olite = Pyolite(admin_repository=admin_repository)

bob = olite.users.create(name='bob', key='my-awesome-key')
alice = olite.users.create(name='alice', key_path='~/.ssh/id_rsa.pub')
