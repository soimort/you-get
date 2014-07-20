#!/usr/bin/env python

import os

def get_head(repo_path):
    """Get (branch, commit) from HEAD of a git repo."""
    ref = open(os.path.join(repo_path, '.git', 'HEAD'), 'r').read().strip()[5:].split('/')
    return ref[-1], open(os.path.join(repo_path, '.git', *ref), 'r').read().strip()[:7]
