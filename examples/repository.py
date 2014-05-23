from pyolite import Pyolite

# initial olite object
admin_repository = '/home/absolute/path/to/gitolite/repo/'
olite = Pyolite(admin_repository=admin_repository)

# create a repo
repo = olite.repos.get('my_repo')
repo = olite.repos.create('ydo')
repo = olite.repos.get_or_create('second_repo')

print "Repo's users: %s" % repo.users

user = olite.users.create(name='bob', key_path="~/.ssh/third_rsa.pub")

# add a new user
repo.users.add(olite.users.get('admin'), permission='W+')
repo.users.add('bob', permission='R')

# change user's permissions
repo.users.edit(olite.users.get('admin'), permission='WR+')
repo.users.edit('bob', permission='RCW')

# remove user
repo.users.remove('admin')
