#!/usr/bin/env python

__all__ = ['coub_download']

from ..common import *
from ..processor import ffmpeg
from ..util.fs import legitimize


def coub_download(url, output_dir='.', merge=True, info_only=False, **kwargs):
    html = get_content(url)

    try:
        json_data = get_coub_data(html)
        title, video_url, audio_url = get_title_and_urls(json_data)
        video_file_name, video_file_path = get_file_path(merge, output_dir, title, video_url)
        audio_file_name, audio_file_path = get_file_path(merge, output_dir, title, audio_url)
        download_url(audio_url, merge, output_dir, title, info_only)
        download_url(video_url, merge, output_dir, title, info_only)
        if not info_only:
            try:
                fix_coub_video_file(video_file_path)
                audio_duration = float(ffmpeg.ffprobe_get_media_duration(audio_file_path))
                video_duration = float(ffmpeg.ffprobe_get_media_duration(video_file_path))
                loop_file_path = get_loop_file_path(title, output_dir)
                single_file_path = audio_file_path
                if audio_duration > video_duration:
                    write_loop_file(round(audio_duration / video_duration), loop_file_path, video_file_name)
                else:
                    single_file_path = audio_file_path
                    write_loop_file(round(video_duration / audio_duration), loop_file_path, audio_file_name)

                ffmpeg.ffmpeg_concat_audio_and_video([loop_file_path, single_file_path], title + "_full", "mp4")
                cleanup_files([video_file_path, audio_file_path, loop_file_path])
            except EnvironmentError as err:
                print("Error preparing full coub video. {}".format(err))
    except Exception as err:
        print("Error while downloading files. {}".format(err))


def write_loop_file(records_number, loop_file_path, file_name):
    with open(loop_file_path, 'a') as file:
        for i in range(records_number):
            file.write("file '{}'\n".format(file_name))


def download_url(url, merge, output_dir, title, info_only):
    mime, ext, size = url_info(url)
    print_info(site_info, title, mime, size)
    if not info_only:
        download_urls([url], title, ext, size, output_dir, merge=merge)


def fix_coub_video_file(file_path):
    with open(file_path, 'r+b') as file:
        file.seek(0)
        file.write(bytes(2))


def get_title_and_urls(json_data):
    title = legitimize(re.sub('[\s*]', "_", json_data['title']))
    video_info = json_data['file_versions']['html5']['video']
    if 'high' not in video_info:
        if 'med' not in video_info:
            video_url = video_info['low']['url']
        else:
            video_url = video_info['med']['url']
    else:
        video_url = video_info['high']['url']
    audio_info = json_data['file_versions']['html5']['audio']
    if 'high' not in audio_info:
        if 'med' not in audio_info:
            audio_url = audio_info['low']['url']
        else:
            audio_url = audio_info['med']['url']
    else:
        audio_url = audio_info['high']['url']
    return title, video_url, audio_url


def get_coub_data(html):
    coub_data = r1(r'<script id=\'coubPageCoubJson\' type=\'text/json\'>([^<]+)</script>', html)
    json_data = json.loads(coub_data)
    return json_data


def get_file_path(merge, output_dir, title, url):
    mime, ext, size = url_info(url)
    file_name = get_output_filename([], title, ext, output_dir, merge)
    file_path = os.path.join(output_dir, file_name)
    return file_name, file_path


def get_loop_file_path(title, output_dir):
    return os.path.join(output_dir, get_output_filename([], title, "txt", None, False))


def cleanup_files(files):
    for file in files:
        os.remove(file)


site_info = "coub.com"
download = coub_download
download_playlist = playlist_not_supported('coub')
