pyolite [![Build Status](https://travis-ci.org/PressLabs/pyolite.svg?branch=master)](https://travis-ci.org/PressLabs/pyolite) [![Coverage Status](https://coveralls.io/repos/PressLabs/pyolite/badge.svg?branch=master)](https://coveralls.io/github/PressLabs/pyolite)
=======

# Welcome to pyolite

pyolite is a Python wrapper for gitolite.

Easy and simple to use, just type `pip install pyolite`.

Using an intuitive API, `pyolite` helps you to easily create users and repos using `gitolite`.

pyolite was developed by the awesome engineering team at [Presslabs](https://www.presslabs.com/), 
a Managed WordPress Hosting provider.

For more open-source projects, check [Presslabs Code](https://www.presslabs.org/). 

## Gitolite Setup Prerequisites

Using Pyolite is very easy, but it requires some initial setup. First, your **gitolite-admin** repo must contain a directory called `repos`, and all `.conf` files in this directory should be included in your `gitolite.conf` file. For example, your **gitolite-admin** repo might have the following structure:

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
repo = olite.repos.create('my_repo')
# get a repo
repo = olite.repos.get('my_repo')
# get or create a repo
repo = olite.repos.get_or_create('second_repo')
```

Every repo has an `users` object, in order to facilitate basic operations: adding, editing and removing users from a repository.
```python
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
```

### Users API

You can easily manipulate `users` as well, using almost the same API.

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
```

### Config API

Gitolite allow users to add extra configurations

```python
repo = olite.repos.get('my_repo')
repo.add_config(("gitolite.mirror.simple", "git@github.com:Presslabs/pyolite.git"))
repo.add_config({
    "gitolite.mirror.simple": "git@github.com:Presslabs/pyolite.git"
})
```

If you need any help with this module, write me `vlad@presslabs.com`
