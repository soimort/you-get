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

#
#params ={"-y":"playlist","-q":None,}
#if Only Key ,Value should be None
#-r -o should not be included in params

def download_rtmpdump_stream(url, title, ext,params={},output_dir='.'):
    filename = '%s.%s' % (title, ext)
    filepath = os.path.join(output_dir, filename)

    cmdline = [RTMPDUMP, '-r']
    cmdline.append(url)
    cmdline.append('-o')
    cmdline.append(filepath)

    for key in params.keys():
        cmdline.append(key)
        if params[key]!=None:
            cmdline.append(params[key])

    # cmdline.append('-y')
    # cmdline.append(playpath)
    print("Call rtmpdump:\n"+" ".join(cmdline)+"\n")
    subprocess.call(cmdline)
    return

#
def play_rtmpdump_stream(player, url, params={}):

    #construct left side of pipe
    rtmp_cmdline = [RTMPDUMP, '-r']
    rtmp_cmdline.append(url)

    #append other params if exist
    for key in params.keys():
        rtmp_cmdline.append(key)
        if params[key] is not None:
            rtmp_cmdline.append(params[key])

    rtmp_cmdline.append('-o')
    rtmp_cmdline.append('-')

    #logging
    print("Call rtmpdump:\n" + " ".join(rtmp_cmdline) + "\n")

    # Safely pipe rtmpdump output to the player using Popen with no shell involvement.
    # Both rtmp_cmdline and player are passed as list arguments (shell=False by default),
    # so no shell interpretation of url or player values occurs.
    rtmp_proc = subprocess.Popen(rtmp_cmdline, stdout=subprocess.PIPE)
    subprocess.call([player, '-'], stdin=rtmp_proc.stdout)
    rtmp_proc.wait()
    return
