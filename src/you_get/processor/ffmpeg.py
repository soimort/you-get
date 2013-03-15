#!/usr/bin/env python

import os.path
import subprocess

def has_ffmpeg_installed():
    try:
        subprocess.call(['ffmpeg', '-loglevel', '0'])
        return True
    except:
        return False

def ffmpeg_convert_ts_to_mkv(files, output = 'output.mkv'):
    for file in files:
        if os.path.isfile(file):
            params = ['ffmpeg', '-i']
            params.append(file)
            params.append(output)
            subprocess.call(params)
    
    return

def ffmpeg_concat_mp4_to_mpg(files, output = 'output.mpg'):
    for file in files:
        if os.path.isfile(file):
            params = ['ffmpeg', '-i']
            params.append(file)
            params.append(file + '.mpg')
            subprocess.call(params)
    
    inputs = [open(file + '.mpg', 'rb') for file in files]
    with open(output + '.mpg', 'wb') as o:
        for input in inputs:
            o.write(input.read())
    
    params = ['ffmpeg', '-i']
    params.append(output + '.mpg')
    params += ['-vcodec', 'copy', '-acodec', 'copy']
    params.append(output)
    subprocess.call(params)
    
    for file in files:
        os.remove(file + '.mpg')
    os.remove(output + '.mpg')
    
    return

def ffmpeg_concat_ts_to_mkv(files, output = 'output.mkv'):
    params = ['ffmpeg', '-isync', '-i']
    params.append('concat:')
    for file in files:
        if os.path.isfile(file):
            params[-1] += file + '|'
    params += ['-f', 'matroska', '-c', 'copy', output]
    
    try:
        if subprocess.call(params) == 0:
            return True
        else:
            return False
    except:
        return False

def ffmpeg_concat_flv_to_mp4(files, output = 'output.mp4'):
    for file in files:
        if os.path.isfile(file):
            params = ['ffmpeg', '-i']
            params.append(file)
            params += ['-map', '0', '-c', 'copy', '-f', 'mpegts', '-bsf:v', 'h264_mp4toannexb']
            params.append(file + '.ts')
            
            subprocess.call(params)
    
    params = ['ffmpeg', '-i']
    params.append('concat:')
    for file in files:
        f = file + '.ts'
        if os.path.isfile(f):
            params[-1] += f + '|'
    params += ['-c', 'copy', '-absf', 'aac_adtstoasc', output]
    
    if subprocess.call(params) == 0:
        for file in files:
            os.remove(file + '.ts')
        return True
    else:
        raise
