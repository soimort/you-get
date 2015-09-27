#!/usr/bin/env python

import os.path
import subprocess

def get_usable_ffmpeg(cmd):
    try:
        p = subprocess.Popen([cmd, '-version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        vers = str(out, 'utf-8').split('\n')[0].split()
        assert (vers[0] == 'ffmpeg' and vers[2][0] > '0') or (vers[0] == 'avconv')
        #if the version is strange like 'N-1234-gd1111', set version to 2.0
        try:
            version = [int(i) for i in vers[2].split('.')]
        except:
            version = [1, 0]
        return cmd, version
    except:
        return None

FFMPEG, FFMPEG_VERSION = get_usable_ffmpeg('ffmpeg') or get_usable_ffmpeg('avconv') or (None, None)

def has_ffmpeg_installed():
    return FFMPEG is not None

def ffmpeg_convert_ts_to_mkv(files, output='output.mkv'):
    for file in files:
        if os.path.isfile(file):
            params = [FFMPEG, '-y', '-i']
            params.append(file)
            params.append(output)
            subprocess.call(params)

    return

def ffmpeg_concat_mp4_to_mpg(files, output='output.mpg'):
    # Use concat demuxer on FFmpeg >= 1.1
    if FFMPEG == 'ffmpeg' and (FFMPEG_VERSION[0] >= 2 or (FFMPEG_VERSION[0] == 1 and FFMPEG_VERSION[1] >= 1)):
        concat_list = open(output + '.txt', 'w', encoding="utf-8")
        for file in files:
            if os.path.isfile(file):
                concat_list.write("file '%s'\n" % file)
        concat_list.close()

        params = [FFMPEG, '-f', 'concat', '-y', '-i']
        params.append(output + '.txt')
        params += ['-c', 'copy', output]

        if subprocess.call(params) == 0:
            os.remove(output + '.txt')
            return True
        else:
            raise

    for file in files:
        if os.path.isfile(file):
            params = [FFMPEG, '-y', '-i']
            params.append(file)
            params.append(file + '.mpg')
            subprocess.call(params)

    inputs = [open(file + '.mpg', 'rb') for file in files]
    with open(output + '.mpg', 'wb') as o:
        for input in inputs:
            o.write(input.read())

    params = [FFMPEG, '-y', '-i']
    params.append(output + '.mpg')
    params += ['-vcodec', 'copy', '-acodec', 'copy']
    params.append(output)
    subprocess.call(params)

    if subprocess.call(params) == 0:
        for file in files:
            os.remove(file + '.mpg')
        os.remove(output + '.mpg')
        return True
    else:
        raise

def ffmpeg_concat_ts_to_mkv(files, output='output.mkv'):
    params = [FFMPEG, '-isync', '-y', '-i']
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

def ffmpeg_concat_flv_to_mp4(files, output='output.mp4'):
    # Use concat demuxer on FFmpeg >= 1.1
    if FFMPEG == 'ffmpeg' and (FFMPEG_VERSION[0] >= 2 or (FFMPEG_VERSION[0] == 1 and FFMPEG_VERSION[1] >= 1)):
        concat_list = open(output + '.txt', 'w', encoding="utf-8")
        for file in files:
            if os.path.isfile(file):
                # for escaping rules, see:
                # https://www.ffmpeg.org/ffmpeg-utils.html#Quoting-and-escaping
                concat_list.write("file '%s'\n" % file.replace("'", r"'\''"))
        concat_list.close()

        params = [FFMPEG, '-f', 'concat', '-y', '-i']
        params.append(output + '.txt')
        params += ['-c', 'copy', output]

        subprocess.check_call(params)
        os.remove(output + '.txt')
        return True

    for file in files:
        if os.path.isfile(file):
            params = [FFMPEG, '-y', '-i']
            params.append(file)
            params += ['-map', '0', '-c', 'copy', '-f', 'mpegts', '-bsf:v', 'h264_mp4toannexb']
            params.append(file + '.ts')

            subprocess.call(params)

    params = [FFMPEG, '-y', '-i']
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

def ffmpeg_concat_mp4_to_mp4(files, output='output.mp4'):
    # Use concat demuxer on FFmpeg >= 1.1
    if FFMPEG == 'ffmpeg' and (FFMPEG_VERSION[0] >= 2 or (FFMPEG_VERSION[0] == 1 and FFMPEG_VERSION[1] >= 1)):
        concat_list = open(output + '.txt', 'w', encoding="utf-8")
        for file in files:
            if os.path.isfile(file):
                concat_list.write("file '%s'\n" % file)
        concat_list.close()

        params = [FFMPEG, '-f', 'concat', '-y', '-i']
        params.append(output + '.txt')
        params += ['-c', 'copy', output]

        if subprocess.call(params) == 0:
            os.remove(output + '.txt')
            return True
        else:
            raise

    for file in files:
        if os.path.isfile(file):
            params = [FFMPEG, '-y', '-i']
            params.append(file)
            params += ['-c', 'copy', '-f', 'mpegts', '-bsf:v', 'h264_mp4toannexb']
            params.append(file + '.ts')

            subprocess.call(params)

    params = [FFMPEG, '-y', '-i']
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
