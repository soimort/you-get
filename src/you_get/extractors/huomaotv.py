#!/usr/bin/env python

__all__ = ['huomaotv_download']

from ..common import *


def get_mobile_room_url(room_id):
    return 'http://www.huomao.com/mobile/mob_live/%s' % room_id


def get_m3u8_url(stream_id):
    return 'http://live-ws.huomaotv.cn/live/%s/playlist.m3u8' % stream_id


def huomaotv_download(url, output_dir='.', merge=True, info_only=False, **kwargs):
    room_id_pattern = r'huomao.com/(\d+)'
    room_id = match1(url, room_id_pattern)
    html = get_content(get_mobile_room_url(room_id))

    stream_id_pattern = r'id="html_stream" value="(\w+)"'
    stream_id = match1(html, stream_id_pattern)

    m3u8_url = get_m3u8_url(stream_id)

    title = match1(html, r'<title>([^<]{1,9999})</title>')

    print_info(site_info, title, 'm3u8', float('inf'))

    if not info_only:
        download_url_ffmpeg(m3u8_url, title, 'm3u8', None, output_dir=output_dir, merge=merge)


site_info = 'huomao.com'
download = huomaotv_download
download_playlist = playlist_not_supported('huomao')
