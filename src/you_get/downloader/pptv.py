#!/usr/bin/env python

__all__ = ['pptv_download', 'pptv_download_by_id']

from ..common import *

import re
import urllib
import hashlib

def pptv_download_by_id(id, title = None, output_dir = '.', merge = True, info_only = False):
    xml = get_html('http://web-play.pptv.com/webplay3-151-%s.xml' % id)
    host = r1(r'<sh>([^<>]+)</sh>', xml)
    port = 8080
    st = r1(r'<st>([^<>]+)</st>', xml).encode('utf-8')
    key = hashlib.md5(st).hexdigest() # FIXME: incorrect key
    rids = re.findall(r'rid="([^"]+)"', xml)
    rid = r1(r'rid="([^"]+)"', xml)
    title = r1(r'nm="([^"]+)"', xml)
    pieces = re.findall('<sgm no="(\d+)".*fs="(\d+)"', xml)
    numbers, fs = zip(*pieces)
    urls = ['http://%s:%s/%s/%s?key=%s' % (host, port, i, rid, key) for i in numbers]
    urls = ['http://pptv.vod.lxdns.com/%s/%s?key=%s' % (i, rid, key) for i in numbers]
    total_size = sum(map(int, fs))
    assert rid.endswith('.mp4')
    
    print_info(site_info, title, 'mp4', total_size)
    if not info_only:
        download_urls(urls, title, 'mp4', total_size, output_dir = output_dir, merge = merge)

def pptv_download(url, output_dir = '.', merge = True, info_only = False):
    assert re.match(r'http://v.pptv.com/show/(\w+)\.html$', url)
    html = get_html(url)
    id = r1(r'webcfg\s*=\s*{"id":\s*(\d+)', html)
    assert id
    pptv_download_by_id(id, output_dir = output_dir, merge = merge, info_only = info_only)

site_info = "PPTV.com"
download = pptv_download
download_playlist = playlist_not_supported('pptv')
