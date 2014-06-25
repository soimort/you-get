#!/usr/bin/env python

__all__ = ['vimeo_download', 'vimeo_download_by_id']

from ..common import *

def vimeo_download_by_id(id, title = None, output_dir = '.', merge = True, info_only = False):
    video_page = get_content('http://player.vimeo.com/video/%s' % id, headers=fake_headers)
    title = r1(r'<title>([^<]+)</title>', video_page)
    info = dict(re.findall(r'"([^"]+)":\{[^{]+"url":"([^"]+)"', video_page))
    for quality in ['hd', 'sd', 'mobile']:
        if quality in info:
            url = info[quality]
            break
    assert url
    
    type, ext, size = url_info(url, faker=True)
    
    print_info(site_info, title, type, size)
    if not info_only:
        download_urls([url], title, ext, size, output_dir, merge = merge, faker = True)

def vimeo_download(url, output_dir = '.', merge = True, info_only = False):
    id = r1(r'http://[\w.]*vimeo.com[/\w]*/(\d+)$', url)
    assert id
    
    vimeo_download_by_id(id, None, output_dir = output_dir, merge = merge, info_only = info_only)

site_info = "Vimeo.com"
download = vimeo_download
download_playlist = playlist_not_supported('vimeo')
