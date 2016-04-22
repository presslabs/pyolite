pyolite [![Build Status](https://travis-ci.org/PressLabs/svg?branch=master)](https://travis-ci.org/PressLabs/pyolite) [![Coverage Status](https://coveralls.io/repos/PressLabs/pyolite/badge.png)](https://coveralls.io/r/PressLabs/pyolite) [![Downloads](https://pypip.in/d/pyolite/badge.png)](https://crate.io/packages/pyolite/)
=======
# Python wrapper for gitolite

Easy and simple to user, just `pip install pyolite` and boom!!!

Using an intuitive API, `pyolite` help you easly create users and repos using `gitolite`.

## Gitolite Setup Prereqs

Using Pyolite is very easy, but requires some initial set up. First, your **gitolite-admin** repo must contain a directory called `repos`, and all `.conf` files in this directory should be included in your `gitolite.conf` file. For example, your **gitolite-admin** repo might have the following structure:

```
├── gitolite.conf
└── repos
    └── [ empty ]
```

And your `gitolite.conf` file might look like this:

```
repo gitolite-admin
    RW+     =   admin

repo testing
    RW+     =   @all

include	    "repos/*.conf"
```

This is required because Pyolite makes changes to files only inside the **repos** directory.

### Repository API

First, we need to initialize a `pyolite` object with the path to `gitolite`'s repository.

```python
from pyolite import Pyolite

# initial olite object
admin_repository = '/home/absolute/path/to/gitolite/repo/'
olite = Pyolite(admin_repository=admin_repository)
```

After that, we can create and get a repo using `create` and `get` methods.

```python
# create a repo
repo = olite.repos.get('my_repo')
repo = olite.repos.create('ydo')
repo = olite.repos.get_or_create('second_repo')

# List existing Pyolite repos
repos = olite.repos.all()
for repo_it in repos:
  print repo_it.name
```

Every repo has an `users` object, in order to facilitate basic operations: adding, editing and removing users from a repository.

```python
print "Repo's users: %s" % repo.users

# list a repo's users
users_as_list = repo.users.list()

user = olite.users.create(name='bob', key_path="~/.ssh/third_rsa.pub")

# add a new user
repo.users.add(olite.users.get('admin'), permission='W+')
repo.users.add('bob', permission='R')

# change user's permissions
repo.users.edit(olite.users.get('admin'), permission='WR+')
repo.users.edit('bob', permission='RCW')

# remove user
repo.users.remove('admin')
```

### Users API

You an easly manipulate `users` aswell, using allmost the same API.

```python
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

# check if user is admin or not
print vlad.is_admin

# list user's keys and repos
keys_as_list = vlad.list_keys()
repos_as_list = vlad.list_repos()

# delete a user by name
deleted_user = olite.users.delete('username')
print deleted_user
```

If you need any help with this module, write me `vlad@presslabs.com`
