#!/usr/bin/env python

__all__ = ['videobam_download']

from ..common import *
import urllib.error
import json

def videobam_download(url, output_dir = '.', merge = True, info_only = False, **kwargs):
    if re.match(r'http://videobam.com/\w+', url):
        #Todo: Change to re. way
        vid = url.split('/')[-1]
        downloadurl = 'http://videobam.com/videos/download/' + vid
        html = get_html(downloadurl)
        downloadPage_list = html.split('\n')
        title = r1(r'<meta property="og:title" content="([^"]*)"', html)
        for i in downloadPage_list:
            if 'ajax_download_url' in i:
                ajaxurl = 'http://videobam.com/videos/ajax_download_url/'+ vid+'/' + i.split('/')[-1][:-2]
                break
        json_class = json.JSONDecoder()
        api_response = json_class.raw_decode(get_html(ajaxurl))
        url = str(api_response[0]['url'])
        type, ext, size = url_info(url)
        print_info(site_info, title, type, size)
        if not info_only:
            download_urls([url], title, ext, size, output_dir, merge=merge)

site_info = "VideoBam"
download = videobam_download
download_playlist = playlist_not_supported('videobam')
