#!/usr/bin/env python

import logging
import os
import subprocess
import sys
from ..util.strings import parameterize
from ..common import print_more_compatible as print

try:
    from subprocess import DEVNULL
except ImportError:
    # Python 3.2 or below
    import os
    import atexit
    DEVNULL = os.open(os.devnull, os.O_RDWR)
    atexit.register(lambda fd: os.close(fd), DEVNULL)

def get_usable_ffmpeg(cmd):
    try:
        p = subprocess.Popen([cmd, '-version'], stdin=DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        vers = str(out, 'utf-8').split('\n')[0].split()
        assert (vers[0] == 'ffmpeg' and vers[2][0] > '0') or (vers[0] == 'avconv')
        try:
            v = vers[2][1:] if vers[2][0] == 'n' else vers[2]
            version = [int(i) for i in v.split('.')]
        except:
            version = [1, 0]
        return cmd, 'ffprobe', version
    except:
        return None

FFMPEG, FFPROBE, FFMPEG_VERSION = get_usable_ffmpeg('ffmpeg') or get_usable_ffmpeg('avconv') or (None, None, None)
if logging.getLogger().isEnabledFor(logging.DEBUG):
    LOGLEVEL = ['-loglevel', 'info']
    STDIN = None
else:
    LOGLEVEL = ['-loglevel', 'quiet']
    STDIN = DEVNULL

def has_ffmpeg_installed():
    return FFMPEG is not None

# Given a list of segments and the output path, generates the concat
# list and returns the path to the concat list.
def generate_concat_list(files, output):
    concat_list_path = output + '.txt'
    concat_list_dir = os.path.dirname(concat_list_path)
    with open(concat_list_path, 'w', encoding='utf-8') as concat_list:
        for file in files:
            if os.path.isfile(file):
                relpath = os.path.relpath(file, start=concat_list_dir)
                concat_list.write('file %s\n' % parameterize(relpath))
    return concat_list_path

def ffmpeg_concat_av(files, output, ext):
    print('Merging video parts... ', end="", flush=True)
    params = [FFMPEG] + LOGLEVEL
    for file in files:
        if os.path.isfile(file): params.extend(['-i', file])
    params.extend(['-c', 'copy'])
    params.append(output)
    if subprocess.call(params, stdin=STDIN):
        print('Merging without re-encode failed.\nTry again re-encoding audio... ', end="", flush=True)
        try: os.remove(output)
        except FileNotFoundError: pass
        params = [FFMPEG] + LOGLEVEL
        for file in files:
            if os.path.isfile(file): params.extend(['-i', file])
        params.extend(['-c:v', 'copy'])
        if ext == 'mp4':
            params.extend(['-c:a', 'aac'])
            params.extend(['-strict', 'experimental'])
        elif ext == 'webm':
            params.extend(['-c:a', 'opus'])
        params.append(output)
        return subprocess.call(params, stdin=STDIN)
    else:
        return 0

def ffmpeg_convert_ts_to_mkv(files, output='output.mkv'):
    for file in files:
        if os.path.isfile(file):
            params = [FFMPEG] + LOGLEVEL
            params.extend(['-y', '-i', file, output])
            subprocess.call(params, stdin=STDIN)

    return

def ffmpeg_concat_mp4_to_mpg(files, output='output.mpg'):
    # Use concat demuxer on FFmpeg >= 1.1
    if FFMPEG == 'ffmpeg' and (FFMPEG_VERSION[0] >= 2 or (FFMPEG_VERSION[0] == 1 and FFMPEG_VERSION[1] >= 1)):
        concat_list = generate_concat_list(files, output)
        params = [FFMPEG] + LOGLEVEL + ['-y', '-f', 'concat', '-safe', '-1',
                                        '-i', concat_list, '-c', 'copy', output]
        if subprocess.call(params, stdin=STDIN) == 0:
            os.remove(output + '.txt')
            return True
        else:
            raise

    for file in files:
        if os.path.isfile(file):
            params = [FFMPEG] + LOGLEVEL + ['-y', '-i']
            params.extend([file, file + '.mpg'])
            subprocess.call(params, stdin=STDIN)

    inputs = [open(file + '.mpg', 'rb') for file in files]
    with open(output + '.mpg', 'wb') as o:
        for input in inputs:
            o.write(input.read())

    params = [FFMPEG] + LOGLEVEL + ['-y', '-i']
    params.append(output + '.mpg')
    params += ['-vcodec', 'copy', '-acodec', 'copy']
    params.append(output)

    if subprocess.call(params, stdin=STDIN) == 0:
        for file in files:
            os.remove(file + '.mpg')
        os.remove(output + '.mpg')
        return True
    else:
        raise

def ffmpeg_concat_ts_to_mkv(files, output='output.mkv'):
    print('Merging video parts... ', end="", flush=True)
    params = [FFMPEG] + LOGLEVEL + ['-isync', '-y', '-i']
    params.append('concat:')
    for file in files:
        if os.path.isfile(file):
            params[-1] += file + '|'
    params += ['-f', 'matroska', '-c', 'copy', output]

    try:
        if subprocess.call(params, stdin=STDIN) == 0:
            return True
        else:
            return False
    except:
        return False

def ffmpeg_concat_flv_to_mp4(files, output='output.mp4'):
    print('Merging video parts... ', end="", flush=True)
    # Use concat demuxer on FFmpeg >= 1.1
    if FFMPEG == 'ffmpeg' and (FFMPEG_VERSION[0] >= 2 or (FFMPEG_VERSION[0] == 1 and FFMPEG_VERSION[1] >= 1)):
        concat_list = generate_concat_list(files, output)
        params = [FFMPEG] + LOGLEVEL + ['-y', '-f', 'concat', '-safe', '-1',
                                        '-i', concat_list, '-c', 'copy',
                                        '-bsf:a', 'aac_adtstoasc', output]
        subprocess.check_call(params, stdin=STDIN)
        os.remove(output + '.txt')
        return True

    for file in files:
        if os.path.isfile(file):
            params = [FFMPEG] + LOGLEVEL + ['-y', '-i']
            params.append(file)
            params += ['-map', '0', '-c', 'copy', '-f', 'mpegts', '-bsf:v', 'h264_mp4toannexb']
            params.append(file + '.ts')

            subprocess.call(params, stdin=STDIN)

    params = [FFMPEG] + LOGLEVEL + ['-y', '-i']
    params.append('concat:')
    for file in files:
        f = file + '.ts'
        if os.path.isfile(f):
            params[-1] += f + '|'
    if FFMPEG == 'avconv':
        params += ['-c', 'copy', output]
    else:
        params += ['-c', 'copy', '-absf', 'aac_adtstoasc', output]

    if subprocess.call(params, stdin=STDIN) == 0:
        for file in files:
            os.remove(file + '.ts')
        return True
    else:
        raise

def ffmpeg_concat_mp4_to_mp4(files, output='output.mp4'):
    print('Merging video parts... ', end="", flush=True)
    # Use concat demuxer on FFmpeg >= 1.1
    if FFMPEG == 'ffmpeg' and (FFMPEG_VERSION[0] >= 2 or (FFMPEG_VERSION[0] == 1 and FFMPEG_VERSION[1] >= 1)):
        concat_list = generate_concat_list(files, output)
        params = [FFMPEG] + LOGLEVEL + ['-y', '-f', 'concat', '-safe', '-1',
                                        '-i', concat_list, '-c', 'copy',
                                        '-bsf:a', 'aac_adtstoasc', output]
        subprocess.check_call(params, stdin=STDIN)
        os.remove(output + '.txt')
        return True

    for file in files:
        if os.path.isfile(file):
            params = [FFMPEG] + LOGLEVEL + ['-y', '-i']
            params.append(file)
            params += ['-c', 'copy', '-f', 'mpegts', '-bsf:v', 'h264_mp4toannexb']
            params.append(file + '.ts')

            subprocess.call(params, stdin=STDIN)

    params = [FFMPEG] + LOGLEVEL + ['-y', '-i']
    params.append('concat:')
    for file in files:
        f = file + '.ts'
        if os.path.isfile(f):
            params[-1] += f + '|'
    if FFMPEG == 'avconv':
        params += ['-c', 'copy', output]
    else:
        params += ['-c', 'copy', '-absf', 'aac_adtstoasc', output]

    subprocess.check_call(params, stdin=STDIN)
    for file in files:
        os.remove(file + '.ts')
    return True

def ffmpeg_download_stream(files, title, ext, params={}, output_dir='.', stream=True):
    """str, str->True
    WARNING: NOT THE SAME PARMS AS OTHER FUNCTIONS!!!!!!
    You can basicly download anything with this function
    but better leave it alone with
    """
    output = title + '.' + ext

    if not (output_dir == '.'):
        output = output_dir + '/' + output

    print('Downloading streaming content with FFmpeg, press q to stop recording...')
    if stream:
        ffmpeg_params = [FFMPEG] + ['-y', '-re', '-i']
    else:
        ffmpeg_params = [FFMPEG] + ['-y', '-i']
    ffmpeg_params.append(files)  #not the same here!!!!

    if FFMPEG == 'avconv':  #who cares?
        ffmpeg_params += ['-c', 'copy', output]
    else:
        ffmpeg_params += ['-c', 'copy', '-bsf:a', 'aac_adtstoasc']

    if params is not None:
        if len(params) > 0:
            for k, v in params:
                ffmpeg_params.append(k)
                ffmpeg_params.append(v)

    ffmpeg_params.append(output)

    print(' '.join(ffmpeg_params))

    try:
        a = subprocess.Popen(ffmpeg_params, stdin= subprocess.PIPE)
        a.communicate()
    except KeyboardInterrupt:
        try:
            a.stdin.write('q'.encode('utf-8'))
        except:
            pass

    return True


def ffmpeg_concat_audio_and_video(files, output, ext):
    print('Merging video and audio parts... ', end="", flush=True)
    if has_ffmpeg_installed:
        params = [FFMPEG] + LOGLEVEL
        params.extend(['-f', 'concat'])
        params.extend(['-safe', '0'])  # https://stackoverflow.com/questions/38996925/ffmpeg-concat-unsafe-file-name
        for file in files:
            if os.path.isfile(file):
                params.extend(['-i', file])
        params.extend(['-c:v', 'copy'])
        params.extend(['-c:a', 'aac'])
        params.extend(['-strict', 'experimental'])
        params.append(output+"."+ext)
        return subprocess.call(params, stdin=STDIN)
    else:
        raise EnvironmentError('No ffmpeg found')


def ffprobe_get_media_duration(file):
    print('Getting {} duration'.format(file))
    params = [FFPROBE]
    params.extend(['-i', file])
    params.extend(['-show_entries', 'format=duration'])
    params.extend(['-v', 'quiet'])
    params.extend(['-of', 'csv=p=0'])
    return subprocess.check_output(params, stdin=STDIN, stderr=subprocess.STDOUT).decode().strip()
