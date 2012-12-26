#!/usr/bin/env python

__all__ = ['xtube_download', 'xtube_download_by_id']

from ..common import *

import urllib

def xtube_download_by_id(id, title = None, output_dir = '.', merge = True, info_only = False):
    html = get_html('http://www.xtube.com/find_video.php?video_id=%s' % id)
    url = urllib.parse.unquote(r1('&filename=([a-zA-Z0-9\-\%\.\\_]+)', html))
    title = "[%s] %s" % (id, title)
    type, ext, size = url_info(url)
    print_info(site_info, title, type, size)
    if not info_only:
        download_urls([url], title, ext, size, output_dir, merge = merge)

def xtube_download(url, output_dir = '.', merge = True, info_only = False):
    html = get_html(url)
    title = r1(r'<title>(.*)</title>', html)
    assert title
    id = r1(r'http://www.xtube.com/watch.php\?v=([a-zA-Z0-9\-]+)', url)
    assert id
    xtube_download_by_id(id, title, output_dir = output_dir, merge = merge, info_only = info_only)
    
site_info = "xtube.com"
download = xtube_download
download_playlist = playlist_not_supported('xtube')
