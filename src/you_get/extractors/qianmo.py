#!/usr/bin/env python

__all__ = ['qianmo_download']

from ..common import *
import urllib.error
import json

def qianmo_download(url, output_dir = '.', merge = False, info_only = False, **kwargs):
    if re.match(r'http://qianmo.com/\w+', url):
        html = get_html(url)
        match = re.search(r'(.+?)var video =(.+?);', html)
        
        if match:
            video_info_json = json.loads(match.group(2))
            title = video_info_json['title']
            ext_video_id = video_info_json['ext_video_id']
        
        html = get_content('http://v.qianmo.com/player/{ext_video_id}'.format(ext_video_id = ext_video_id))
        c = json.loads(html)
        url_list = []
        for i in c['seg']:  #Cannot do list comprehensions
            for a in c['seg'][i]:
                for b in a['url']:
                    url_list.append(b[0])
        
        type_ = ''
        size = 0
        for url in url_list:
            _, type_, temp = url_info(url)
            size += temp

        type, ext, size = url_info(url)
        print_info(site_info, title, type_, size)
        if not info_only:
            download_urls(url_list, title, type_, total_size=None, output_dir=output_dir, merge=merge)

site_info = "qianmo"
download = qianmo_download
download_playlist = playlist_not_supported('qianmo')
