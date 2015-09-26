#!/usr/bin/env python

__all__ = ['mixcloud_download']

from ..common import *

def mixcloud_download(url, output_dir = '.', merge = True, info_only = False, **kwargs):
    html = get_html(url)
    title = r1(r'<meta property="og:title" content="([^"]*)"', html)
    preview_url = r1("m-preview=\"([^\"]+)\"", html)

    url = re.sub(r'previews', r'c/originals', preview_url)
    for i in range(10, 30):
        url = re.sub(r'stream[^.]*', r'stream' + str(i), url)

        try:
            type, ext, size = url_info(url)
            break
        except:
            continue

    try:
        type
    except:
        url = re.sub('c/originals', r'c/m4a/64', url)
        url = re.sub('.mp3', '.m4a', url)
        for i in range(10, 30):
            url = re.sub(r'stream[^.]*', r'stream' + str(i), url)

            try:
                type, ext, size = url_info(url)
                break
            except:
                continue

    print_info(site_info, title, type, size)
    if not info_only:
        download_urls([url], title, ext, size, output_dir, merge = merge)

site_info = "Mixcloud.com"
download = mixcloud_download
download_playlist = playlist_not_supported('mixcloud')
