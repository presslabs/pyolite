from pyolite import Pyolite

# initial olite object
admin_repository = '/home/wok/presslabs/pyolite/gitolite-admin/'
olite = Pyolite(admin_repository=admin_repository)

# create a repo
repo = olite.repos.get('oxygen')
# repo = olite.repos.create('ydo')
repo = olite.repos.get_or_create('yo')

print "Repo's users: %s" % repo.users

user = olite.users.create(name='bob', key_path="~/.ssh/third_rsa.pub")

# add a new user
repo.users.add(olite.users.get('key'), permission='W+')
repo.users.add('bob', permission='R')

# change user's permissions
repo.users.edit(olite.users.get('key'), permission='WR+')
repo.users.edit('bob', permission='RCW')

# remove user
repo.users.remove('key')
