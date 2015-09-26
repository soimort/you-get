#!/usr/bin/env python

__all__ = ['baomihua_download', 'baomihua_download_by_id']

from ..common import *

import urllib

def baomihua_download_by_id(id, title = None, output_dir = '.', merge = True, info_only = False, **kwargs):
    html = get_html('http://play.baomihua.com/getvideourl.aspx?flvid=%s' % id)
    host = r1(r'host=([^&]*)', html)
    assert host
    type = r1(r'videofiletype=([^&]*)', html)
    assert type
    vid = r1(r'&stream_name=([0-9\/]+)&', html)
    assert vid
    url = "http://%s/pomoho_video/%s.%s" % (host, vid, type)
    _, ext, size = url_info(url)
    print_info(site_info, title, type, size)
    if not info_only:
        download_urls([url], title, ext, size, output_dir, merge = merge)

def baomihua_download(url, output_dir = '.', merge = True, info_only = False):
    html = get_html(url)
    title = r1(r'<title>(.*)</title>', html)
    assert title
    id = r1(r'flvid=(\d+)', html)
    assert id
    baomihua_download_by_id(id, title, output_dir = output_dir, merge = merge, info_only = info_only)

site_info = "baomihua.com"
download = baomihua_download
download_playlist = playlist_not_supported('baomihua')
