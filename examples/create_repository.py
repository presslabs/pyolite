from pyolite import Pyolite

# initial olite object
olite = Pyolite(repository='~/presslabs/ansible-playbooks/gitolite-admin')

# create a repo
repo = olite.repo('awesome_name')

# add a new user to repo
repo.add_user('bob', permissions='RW+', path_key='~/.ssh/id_rsa.pub',
              raw_key='my-awesome-key')
# add an existing user to repo
repo.add_user('alice')

# show users from repos
print repo.users

# remove user
repo.remove_user('bob')
