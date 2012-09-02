#!/usr/bin/env python

__all__ = ['vimeo_download', 'vimeo_download_by_id']

from ..common import *

def vimeo_download_by_id(id, title = None, output_dir = '.', merge = True, info_only = False):
    html = get_html('http://vimeo.com/%s' % id, faker = True)
    
    signature = r1(r'"signature":"([^"]+)"', html)
    timestamp = r1(r'"timestamp":([^,]+)', html)
    
    title = r1(r'"title":"([^"]+)"', html)
    title = escape_file_path(title)
    
    url = 'http://player.vimeo.com/play_redirect?clip_id=%s&sig=%s&time=%s' % (id, signature, timestamp)
    type, ext, size = url_info(url, faker = True)
    
    print_info(site_info, title, type, size)
    if not info_only:
        download_urls([url], title, ext, size, output_dir, merge = merge, faker = True)

def vimeo_download(url, output_dir = '.', merge = True, info_only = False):
    id = r1(r'http://\w*vimeo.com[/\w]*/(\d+)$', url)
    assert id
    
    vimeo_download_by_id(id, None, output_dir = output_dir, merge = merge, info_only = info_only)

site_info = "Vimeo.com"
download = vimeo_download
download_playlist = playlist_not_supported('vimeo')
