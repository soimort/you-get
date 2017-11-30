#!/usr/bin/env python

__all__ = ['ted_download']

from ..common import *
import json

def ted_download(url, output_dir='.', merge=True, info_only=False, **kwargs):
    html = get_html(url)
    patt = r'"__INITIAL_DATA__"\s*:\s*\{(.+)\}'
    metadata = json.loads('{' + match1(html, patt) + '}')
    title = metadata['talks'][0]['title']
    nativeDownloads = metadata['talks'][0]['downloads']['nativeDownloads']
    for quality in ['high', 'medium', 'low']:
        if quality in nativeDownloads:
            url = nativeDownloads[quality]
            type, ext, size = url_info(url)
            print_info(site_info, title, type, size)
            if not info_only:
                download_urls([url], title, ext, size, output_dir, merge=merge)
            break

site_info = "TED.com"
download = ted_download
download_playlist = playlist_not_supported('ted')
