#!/usr/bin/env python

__all__ = ['acfun_download']

from ..common import *

from .sina import sina_download_by_id
from .tudou import tudou_download_by_iid
from .youku import youku_download_by_id

import json, re

def get_srt_json(id):
    url = 'http://comment.acfun.tv/%s.json' % id
    return get_html(url)

def qq_download_by_id(id, title = None, output_dir = '.', merge = True, info_only = False):
    url = 'http://vsrc.store.qq.com/%s.flv' % id
    assert title
    _, _, size = url_info(url)
    
    print_info(site_info, title, 'flv', size)
    if not info_only:
        download_urls([url], title, 'flv', size, output_dir = output_dir, merge = merge)

def acfun_download_by_id(id, title = None, output_dir = '.', merge = True, info_only = False):
    info = json.loads(get_html('http://www.acfun.tv/api/getVideoByID.aspx?vid=' + id))
    t = info['vtype']
    vid = info['vid']
    if t == 'sina':
        sina_download_by_id(vid, title, output_dir = output_dir, merge = merge, info_only = info_only)
    elif t == 'youku':
        youku_download_by_id(vid, title, output_dir = output_dir, merge = merge, info_only = info_only)
    elif t == 'tudou':
        tudou_download_by_iid(vid, title, output_dir = output_dir, merge = merge, info_only = info_only)
    elif t == 'qq':
        qq_download_by_id(vid, title, output_dir = output_dir, merge = merge, info_only = info_only)
    else:
        raise NotImplementedError(t)
    
    if not info_only:
        print('Downloading %s ...' % (title + '.cmt.json'))
        cmt = get_srt_json(vid)
        with open(title + '.cmt.json', 'w') as x:
            x.write(cmt)

def acfun_download(url, output_dir = '.', merge = True, info_only = False):
    assert re.match(r'http://www.acfun.tv/v/ac(\d+)', url)
    html = get_html(url)
    
    title = r1(r'<h1 id="title-article" class="title"[^<>]*>([^<>]+)<span', html)
    assert title
    title = unescape_html(title)
    title = escape_file_path(title)
    title = title.replace(' - AcFun.tv', '')
    
    id = r1(r"\[Video\](\d+)\[/Video\]", html) or r1(r"\[video\](\d+)\[/video\]", html)
    if not id:
        id = r1(r"src=\"/newflvplayer/player.swf\?id=(\d+)", html)
        
        sina_download_by_id(id, title, output_dir = output_dir, merge = merge, info_only = info_only)
    else:
        acfun_download_by_id(id, title, output_dir = output_dir, merge = merge, info_only = info_only)

site_info = "AcFun.tv"
download = acfun_download
download_playlist = playlist_not_supported('acfun')
