#!/usr/bin/env python

import os.path
import subprocess

def get_usable_rtmpdump(cmd):
    try:
        p = subprocess.Popen([cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        return cmd
    except:
        return None

RTMPDUMP = get_usable_rtmpdump('rtmpdump')

def has_rtmpdump_installed():
    return RTMPDUMP is not None

def download_rtmpdump_stream(url, playpath, title, ext, output_dir='.'):
    filename = '%s.%s' % (title, ext)
    filepath = os.path.join(output_dir, filename)

    params = [RTMPDUMP, '-r']
    params.append(url)
    params.append('-y')
    params.append(playpath)
    params.append('-o')
    params.append(filepath)

    subprocess.call(params)
    return

def play_rtmpdump_stream(player, url, playpath):
    os.system("rtmpdump -r '%s' -y '%s' -o - | %s -" % (url, playpath, player))
    return
