#!/usr/bin/env python

__all__ = ['otomads_download']

from ..common import *
import json

def otomads_download(url, output_dir = '.', merge = False, info_only = False, **kwargs):
    vid = match1(url, r"http://otomads.com/om(\d+)")
    interface_url = "https://otomads.com/api/?type=get_video_info&id={vid}".format(vid = vid)
    rawjson = get_content(interface_url)
    jsonobj = json.loads(rawjson)
    if 'title' in kwargs and kwargs['title']:
        title = kwargs['title']
    else:
         title = jsonobj['title']
    url = jsonobj['url']
    type_ = ''
    size = 0
    _, type_, temp = url_info(url)
    size += temp
    print_info(site_info, title, type_, size)
    if not info_only:
        download_urls([url], title, type_, total_size = None, output_dir = output_dir, merge = merge)

site_info = "otomads.com"
download = otomads_download
download_playlist = playlist_not_supported("otomads")
