from pyolite import Pyolite

# initial olite object
admin_repository = '~/presslabs/ansible-playbooks/gitolite-admin'
olite = Pyolite(admin_repository=admin_repository)

# create a repo
repo = olite.repos.get_or_create('awesome_name')
repo = olite.repos.get('awesome_name')
repo = olite.repos.create('awesome_name')

# add a new user to repo
repo.users.add('bob', permissions='RW+', path_key='~/.ssh/id_rsa.pub',
               raw_key='my-awesome-key')
# add an existing user to repo
repo.users.add('alice')

# show users from repos
print repo.users.all()

# remove user
repo.users.delete('alice')
