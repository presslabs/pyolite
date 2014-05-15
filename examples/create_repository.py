from pyolite import Pyolite

# initial olite object
admin_repository = '~/presslabs/ansible-playbooks/gitolite-admin'
olite = Pyolite(admin_repository=admin_repository)

# create a repo
repo = olite.repos.get_or_create('awesome_name')
repo = olite.repos.get('awesome_name')
repo = olite.repos.create('awesome_name')

# add a new user to repo
bob = repo.users.add('bob', permissions='RW+', key_path='~/.ssh/id_rsa.pub',
                     key='my-awesome-key')
# add an existing user to repo
repo.users.add('alice', permission='R')

repo.users.modify('alice', permission='W+')

# show users from repos
print repo.users.all()

# remove user
repo.users.delete('alice')


alice = olite.users.get_or_create('alice')
# alice.keys.append('key1')
# alice.repos => list
