#!/usr/bin/env python

__all__ = ['vid48_download']

from ..common import *

def vid48_download(url, output_dir = '.', merge = True, info_only = False, **kwargs):
    vid = r1(r'v=([^&]*)', url)
    p_url = "http://vid48.com/embed_player.php?vid=%s&autoplay=yes" % vid
    
    html = get_html(p_url)
    
    title = r1(r'<title>(.*)</title>', html)
    url = "http://vid48.com%s" % r1(r'file: "([^"]*)"', html)
    type, ext, size = url_info(url)
    
    print_info(site_info, title, type, size)
    if not info_only:
        download_urls([url], title, ext, size, output_dir, merge = merge)

site_info = "VID48"
download = vid48_download
download_playlist = playlist_not_supported('vid48')
