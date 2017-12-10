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
    cmdline = [RTMPDUMP, '-r']
    cmdline.append(url)
    
    #append other params if exist
    for key in params.keys():
        cmdline.append(key)
        if params[key]!=None:
            cmdline.append(params[key])

    cmdline.append('-o')
    cmdline.append('-')

    #pipe start
    cmdline.append('|')
    cmdline.append(player)
    cmdline.append('-')

    #logging
    print("Call rtmpdump:\n"+" ".join(cmdline)+"\n")

    #call RTMPDump!
    subprocess.call(cmdline)
    
    # os.system("rtmpdump -r '%s' -y '%s' -o - | %s -" % (url, playpath, player))
    return
