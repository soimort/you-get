#!/usr/bin/env python

__all__ = ['magisto_download']

from ..common import *
import json

def magisto_download(url, output_dir='.', merge=True, info_only=False, **kwargs):
    html = get_html(url)
    
    video_hash = r1(r'video\/([a-zA-Z0-9]+)', url)
    api_url = 'https://www.magisto.com/api/video/{}'.format(video_hash)
    content = get_html(api_url)
    data = json.loads(content)
    title1 = data['title']
    title2 = data['creator']
    title = "%s - %s" % (title1, title2)
    url = data['video_direct_url']
    type, ext, size = url_info(url)

    print_info(site_info, title, type, size)
    if not info_only:
        download_urls([url], title, ext, size, output_dir, merge=merge)

site_info = "Magisto.com"
download = magisto_download
download_playlist = playlist_not_supported('magisto')
