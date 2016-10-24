from __future__ import absolute_import

import os

from sh import git


class Git(object):
    def __init__(self, repo):
        self.repo = repo

    def commit(self, objects, message):
        # validate commit message
        if not message or not isinstance(message, basestring):
            raise ValueError(
                "Commit message should not be empty or not string")

        env = os.environ.copy()
        env.update({
            'GIT_WORK_TREE': self.repo,
            'GIT_DIR': '%s/.git' % self.repo,
        })

        git.gc("--prune --force", _env=env)
        git.checkout("HEAD", _env=env)

        # pull and push from and to the remote
        git.pull("origin", "master", _env=env)

        for obj in objects:
            git.add("-A", obj, _env=env)

        try:
            git.commit("-m", message, _env=env)
        except Exception:
            pass

        git.push(_env=env)
