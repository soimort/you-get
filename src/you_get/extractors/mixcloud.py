#!/usr/bin/env python

__all__ = ['mixcloud_download']

from ..common import *

def mixcloud_download(url, output_dir='.', merge=True, info_only=False, **kwargs):
    html = get_html(url, faker=True)
    title = r1(r'<meta property="og:title" content="([^"]*)"', html)
    preview_url = r1(r'm-preview=\"([^\"]+)\"', html)
    preview = r1(r'previews(.*)\.mp3$', preview_url)

    for i in range(10, 30):
        url = 'https://stream{i}.mixcloud.com/c/m4a/64{p}.m4a'.format(
            i = i,
            p = preview
        )
        try:
            mime, ext, size = url_info(url)
            break
        except: continue

    print_info(site_info, title, ext, size)
    if not info_only:
        download_urls([url], title, ext, size, output_dir=output_dir, merge=merge)

site_info = "Mixcloud.com"
download = mixcloud_download
download_playlist = playlist_not_supported('mixcloud')
