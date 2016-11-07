#!/usr/bin/env python

__all__ = ['ku6_download', 'ku6_download_by_id']

from ..common import *

import json
import re

def ku6_download_by_id(id, title = None, output_dir = '.', merge = True, info_only = False):
    data = json.loads(get_html('http://v.ku6.com/fetchVideo4Player/%s...html' % id))['data']
    t = data['t']
    f = data['f']
    title = title or t
    assert title
    urls = f.split(',')
    ext = re.sub(r'.*\.', '', urls[0])
    assert ext in ('flv', 'mp4', 'f4v'), ext
    ext = {'f4v': 'flv'}.get(ext, ext)
    size = 0
    for url in urls:
        _, _, temp = url_info(url)
        size += temp
    
    print_info(site_info, title, ext, size)
    if not info_only:
        download_urls(urls, title, ext, size, output_dir, merge = merge)

def ku6_download(url, output_dir = '.', merge = True, info_only = False, **kwargs):
    id = None

    if match1(url, r'http://baidu.ku6.com/watch/(.*)\.html') is not None:
        id = baidu_ku6(url)
    else:
        patterns = [r'http://v.ku6.com/special/show_\d+/(.*)\.\.\.html',
                r'http://v.ku6.com/show/(.*)\.\.\.html',
                r'http://my.ku6.com/watch\?.*v=(.*)\.\..*']
        id = r1_of(patterns, url)

    ku6_download_by_id(id, output_dir = output_dir, merge = merge, info_only = info_only)

def baidu_ku6(url):
    id = None

    h1 = get_html(url)
    isrc = match1(h1, r'<iframe id="innerFrame" src="([^"]*)"')

    if isrc is not None:
        h2 = get_html(isrc)
        id = match1(h2, r'http://v.ku6.com/show/(.*)\.\.\.html')

    return id

site_info = "Ku6.com"
download = ku6_download
download_playlist = playlist_not_supported('ku6')
