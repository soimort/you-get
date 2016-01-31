#!/usr/bin/env python

__all__ = ['miaopai_download']

from ..common import *
import urllib.error

def miaopai_download(url, output_dir = '.', merge = False, info_only = False, **kwargs):
    '''Source: Android mobile'''
    if re.match(r'http://video.weibo.com/show\?fid=(\d{4}:\w{32})\w*', url):
        fake_headers_mobile = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'UTF-8,*;q=0.5',
            'Accept-Encoding': 'gzip,deflate,sdch',
            'Accept-Language': 'en-US,en;q=0.8',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 4.4.2; Nexus 4 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.114 Mobile Safari/537.36'
        }
        webpage_url = re.search(r'(http://video.weibo.com/show\?fid=\d{4}:\w{32})\w*', url).group(1) + '&type=mp4'  #mobile

        #grab download URL
        a = get_content(webpage_url, headers= fake_headers_mobile , decoded=True)
        url = match1(a, r'<video src="(.*?)\"\W')

        #grab title
        b = get_content(webpage_url)  #normal
        title = match1(b, r'<meta name="description" content="([\s\S]*?)\"\W')

        type_, ext, size = url_info(url)
        print_info(site_info, title, type_, size)
        if not info_only:
            download_urls([url], title, ext, total_size=None, output_dir=output_dir, merge=merge)


site_info = "miaopai"
download = miaopai_download
download_playlist = playlist_not_supported('miaopai')
