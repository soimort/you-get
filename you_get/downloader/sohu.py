#!/usr/bin/env python

__all__ = ['sohu_download']

from ..common import *

def real_url(host, prot, file, new):
    url = 'http://%s/?prot=%s&file=%s&new=%s' % (host, prot, file, new)
    start, _, host, key, _, _ = get_html(url).split('|')
    return '%s%s?key=%s' % (start[:-1], new, key)

def sohu_download(url, output_dir = '.', merge = True, info_only = False):
    vid = r1('vid="(\d+)"', get_html(url))
    assert vid
    import json
    data = json.loads(get_decoded_html('http://hot.vrs.sohu.com/vrs_flash.action?vid=%s' % vid))
    host = data['allot']
    prot = data['prot']
    urls = []
    data = data['data']
    title = data['tvName']
    size = sum(data['clipsBytes'])
    assert len(data['clipsURL']) == len(data['clipsBytes']) == len(data['su'])
    for file, new in zip(data['clipsURL'], data['su']):
        urls.append(real_url(host, prot, file, new))
    assert data['clipsURL'][0].endswith('.mp4')
    
    print_info(site_info, title, 'mp4', size)
    if not info_only:
        download_urls(urls, title, 'mp4', size, output_dir, refer = url, merge = merge)

site_info = "Sohu.com"
download = sohu_download
download_playlist = playlist_not_supported('sohu')
