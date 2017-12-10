#!/usr/bin/env python

import os
import subprocess
from ..version import __version__

def get_head(repo_path):
    """Get (branch, commit) from HEAD of a git repo."""
    try:
        ref = open(os.path.join(repo_path, '.git', 'HEAD'), 'r').read().strip()[5:].split('/')
        branch = ref[-1]
        commit = open(os.path.join(repo_path, '.git', *ref), 'r').read().strip()[:7]
        return branch, commit
    except:
        return None

def get_version(repo_path):
    try:
        version = __version__.split('.')
        major, minor, cn = [int(i) for i in version]
        p = subprocess.Popen(['git',
                              '--git-dir', os.path.join(repo_path, '.git'),
                              '--work-tree', repo_path,
                              'rev-list', 'HEAD', '--count'],
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        raw, err = p.communicate()
        c_head = int(raw.decode('ascii'))
        q = subprocess.Popen(['git',
                              '--git-dir', os.path.join(repo_path, '.git'),
                              '--work-tree', repo_path,
                              'rev-list', 'master', '--count'],
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        raw, err = q.communicate()
        c_master = int(raw.decode('ascii'))
        cc = c_head - c_master
        assert cc
        return '%s.%s.%s' % (major, minor, cn + cc)
    except:
        return __version__
