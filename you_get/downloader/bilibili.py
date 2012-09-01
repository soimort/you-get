#!/usr/bin/env python

__all__ = ['bilibili_download']

from ..common import *

from .sina import sina_download_by_id
from .tudou import tudou_download_by_id
from .youku import youku_download_by_id

import re

def get_srt_xml(id):
    url = 'http://comment.bilibili.tv/dm,%s' % id
    return get_html(url)

def parse_srt_p(p):
    fields = p.split(',')
    assert len(fields) == 8, fields
    time, mode, font_size, font_color, pub_time, pool, user_id, history = fields
    time = float(time)
    
    mode = int(mode)
    assert 1 <= mode <= 8
    # mode 1~3: scrolling
    # mode 4: bottom
    # mode 5: top
    # mode 6: reverse?
    # mode 7: position
    # mode 8: advanced
    
    pool = int(pool)
    assert 0 <= pool <= 2
    # pool 0: normal
    # pool 1: srt
    # pool 2: special?
    
    font_size = int(font_size)
    
    font_color = '#%06x' % int(font_color)
    
    return pool, mode, font_size, font_color

def parse_srt_xml(xml):
    d = re.findall(r'<d p="([^"]+)">(.*)</d>', xml)
    for x, y in d:
        p = parse_srt_p(x)
    raise NotImplementedError()

def bilibili_download(url, output_dir = '.', merge = True, info_only = False):
    assert re.match(r'http://(www.bilibili.tv|bilibili.kankanews.com)/video/av(\d+)', url)
    html = get_html(url)
    
    title = r1(r'<h2>([^<>]+)</h2>', html)
    title = unescape_html(title)
    title = escape_file_path(title)
    
    flashvars = r1(r'flashvars="([^"]+)"', html)
    assert flashvars
    t, id = flashvars.split('=', 1)
    if t == 'vid':
        sina_download_by_id(id, title, output_dir = output_dir, merge = merge, info_only = info_only)
    elif t == 'ykid':
        youku_download_by_id(id, title, output_dir = output_dir, merge = merge, info_only = info_only)
    elif t == 'uid':
        tudou_download_by_id(id, title, output_dir = output_dir, merge = merge, info_only = info_only)
    else:
        raise NotImplementedError(flashvars)
    
    #xml = get_srt_xml(id)
    #with open(title + '.xml', 'w') as x:
    #    x.write(xml.encode('utf-8'))

site_info = "bilibili.tv"
download = bilibili_download
download_playlist = playlist_not_supported('bilibili')
