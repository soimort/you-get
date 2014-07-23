#!/usr/bin/env python

import os

def get_head(repo_path):
    """Get (branch, commit) from HEAD of a git repo."""
    try:
        ref = open(os.path.join(repo_path, '.git', 'HEAD'), 'r').read().strip()[5:].split('/')
        branch = ref[-1]
        commit = open(os.path.join(repo_path, '.git', *ref), 'r').read().strip()[:7]
        return branch, commit
    except:
        return None
