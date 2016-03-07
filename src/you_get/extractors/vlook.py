#!/usr/bin/env python

__all__ = ['vlook_download']

from ..common import *
import urllib.error

def vlook_download_by_url(url, output_dir = '.', merge = False, info_only = False, **kwargs):
    '''Source: Android mobile'''
    if re.match(r'http://www.vlook.cn/show/qs/.+', url):
        fake_headers_mobile = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'UTF-8,*;q=0.5',
            'Accept-Encoding': 'gzip,deflate,sdch',
            'Accept-Language': 'en-US,en;q=0.8',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 4.4.2; Nexus 4 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.114 Mobile Safari/537.36'
        }
        
        #grab download URL
        a = get_content(url, headers= fake_headers_mobile , decoded=True)
        url = match1(a, r'<source src="(.*?)\"\W')

        #grab title
        title = match1(a, r'<meta name="description" content="([\s\S]*?)\"\W')

        type_, ext, size = url_info(url)
        print_info(site_info, title, type_, size)
        if not info_only:
            download_urls([url], title, ext, total_size=None, output_dir=output_dir, merge=merge)

#----------------------------------------------------------------------
def vlook_download(url, output_dir = '.', merge = False, info_only = False, **kwargs):
    """"""
    if re.match(r'http://www.vlook.cn/show/qs/.+', url):
        vlook_download_by_url(url, output_dir, merge, info_only)

site_info = "vlook"
download = vlook_download
download_playlist = playlist_not_supported('vlook')
