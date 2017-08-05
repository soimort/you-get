#!/usr/bin/env python

__all__ = ['iqilu_download']

from ..common import *
import json

def iqilu_download(url, output_dir = '.', merge = False, info_only = False, **kwargs):
    ''''''
    if re.match(r'http://v.iqilu.com/\w+', url):
        patt = r'url\s*:\s*\[([^\]]+)\]'
        
        #URL in webpage
        html = get_content(url)
        player_data = '[' + match1(html, patt) + ']'
        urls = json.loads(player_data)
        url = urls[0]['stream_url']
        
        #grab title
        title = match1(html, r'<meta name="description" content="(.*?)\"\W')

        type_, ext, size = url_info(url)
        print_info(site_info, title, type_, size)
        if not info_only:
            download_urls([url], title, ext, total_size=None, output_dir=output_dir, merge=merge)


site_info = "iQilu"
download = iqilu_download
download_playlist = playlist_not_supported('iqilu')
