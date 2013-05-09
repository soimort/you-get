#!/usr/bin/env python

import os.path
import subprocess

def get_usable_ffmpeg(cmd):
    try:
        p = subprocess.Popen([cmd, '-version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        vers = str(out, 'utf-8').split('\n')[0].split(' ')
        assert (vers[0] == 'ffmpeg' and vers[2][0] > '0') or (vers[0] == 'avconv')
        return cmd
    except:
        return None

FFMPEG = get_usable_ffmpeg('ffmpeg') or get_usable_ffmpeg('avconv')

def has_ffmpeg_installed():
    return FFMPEG is not None

def ffmpeg_convert_ts_to_mkv(files, output = 'output.mkv'):
    for file in files:
        if os.path.isfile(file):
            params = [FFMPEG, '-i']
            params.append(file)
            params.append(output)
            subprocess.call(params)
    
    return

def ffmpeg_concat_mp4_to_mpg(files, output = 'output.mpg'):
    for file in files:
        if os.path.isfile(file):
            params = [FFMPEG, '-i']
            params.append(file)
            params.append(file + '.mpg')
            subprocess.call(params)
    
    inputs = [open(file + '.mpg', 'rb') for file in files]
    with open(output + '.mpg', 'wb') as o:
        for input in inputs:
            o.write(input.read())
    
    params = [FFMPEG, '-i']
    params.append(output + '.mpg')
    params += ['-vcodec', 'copy', '-acodec', 'copy']
    params.append(output)
    subprocess.call(params)
    
    for file in files:
        os.remove(file + '.mpg')
    os.remove(output + '.mpg')
    
    return

def ffmpeg_concat_ts_to_mkv(files, output = 'output.mkv'):
    params = [FFMPEG, '-isync', '-i']
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
            params = [FFMPEG, '-i']
            params.append(file)
            params += ['-map', '0', '-c', 'copy', '-f', 'mpegts', '-bsf:v', 'h264_mp4toannexb']
            params.append(file + '.ts')
            
            subprocess.call(params)
    
    params = [FFMPEG, '-i']
    params.append('concat:')
    for file in files:
        f = file + '.ts'
        if os.path.isfile(f):
            params[-1] += f + '|'
    if FFMPEG == 'avconv':
        params += ['-c', 'copy', output]
    else:
        params += ['-c', 'copy', '-absf', 'aac_adtstoasc', output]
    
    if subprocess.call(params) == 0:
        for file in files:
            os.remove(file + '.ts')
        return True
    else:
        raise

def ffmpeg_concat_mp4_to_mp4(files, output = 'output.mp4'):
    for file in files:
        if os.path.isfile(file):
            params = [FFMPEG, '-i']
            params.append(file)
            params += ['-c', 'copy', '-f', 'mpegts', '-bsf:v', 'h264_mp4toannexb']
            params.append(file + '.ts')
            
            subprocess.call(params)
    
    params = [FFMPEG, '-i']
    params.append('concat:')
    for file in files:
        f = file + '.ts'
        if os.path.isfile(f):
            params[-1] += f + '|'
    if FFMPEG == 'avconv':
        params += ['-c', 'copy', output]
    else:
        params += ['-c', 'copy', '-absf', 'aac_adtstoasc', output]
    
    if subprocess.call(params) == 0:
        for file in files:
            os.remove(file + '.ts')
        return True
    else:
        raise
