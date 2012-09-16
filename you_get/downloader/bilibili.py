#!/usr/bin/env python

__all__ = ['bilibili_download']

from ..common import *

from .sina import sina_download_by_id
from .tudou import tudou_download_by_id
from .youku import youku_download_by_id

import re

def get_srt_xml(id):
    url = 'http://comment.bilibili.tv/%s.xml' % id
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

def parse_cid_playurl(xml):
    from xml.dom.minidom import parseString
    doc = parseString(xml.encode('utf-8'))
    urls = [durl.getElementsByTagName('url')[0].firstChild.nodeValue for durl in doc.getElementsByTagName('durl')]
    return urls

def bilibili_download_by_cid(id, title, output_dir = '.', merge = True, info_only = False):
    url = 'http://interface.bilibili.tv/playurl?cid=' + id
    urls = parse_cid_playurl(get_html(url, 'utf-8'))
    assert re.search(r'\.(flv|hlv)\b', urls[0]), urls[0]
    
    size = 0
    for url in urls:
        _, _, temp = url_info(url)
        size += temp
    
    print_info(site_info, title, 'flv', size)
    if not info_only:
        download_urls(urls, title, 'flv', total_size = None, output_dir = output_dir, merge = merge)

def bilibili_download(url, output_dir = '.', merge = True, info_only = False):
    assert re.match(r'http://(www.bilibili.tv|bilibili.kankanews.com)/video/av(\d+)', url)
    html = get_html(url)
    
    title = r1(r'<h2>([^<>]+)</h2>', html)
    title = unescape_html(title)
    title = escape_file_path(title)
    
    flashvars = r1_of([r'flashvars="([^"]+)"', r'"https://secure.bilibili.tv/secure,(cid=\d+)"'], html)
    assert flashvars
    t, id = flashvars.split('=', 1)
    if t == 'cid':
        bilibili_download_by_cid(id, title, output_dir = output_dir, merge = merge, info_only = info_only)
    elif t == 'vid':
        sina_download_by_id(id, title, output_dir = output_dir, merge = merge, info_only = info_only)
    elif t == 'ykid':
        youku_download_by_id(id, title, output_dir = output_dir, merge = merge, info_only = info_only)
    elif t == 'uid':
        tudou_download_by_id(id, title, output_dir = output_dir, merge = merge, info_only = info_only)
    else:
        raise NotImplementedError(flashvars)
    
    if not info_only:
        print('Downloading %s ...' % (title + '.cmt.xml'))
        xml = get_srt_xml(id)
        with open(title + '.cmt.xml', 'w') as x:
            x.write(xml)

site_info = "bilibili.tv"
download = bilibili_download
download_playlist = playlist_not_supported('bilibili')
