#!/usr/bin/env python
# -*- coding: utf-8 -*-

__all__ = ['youku_download', 'youku_download_playlist', 'youku_download_by_id']

from ..common import *

import json
from random import randint
from time import time
import re
import sys

def trim_title(title):
    title = title.replace(' - 视频 - 优酷视频 - 在线观看', '')
    title = title.replace(' - 专辑 - 优酷视频', '')
    title = re.sub(r'—([^—]+)—优酷网，视频高清在线观看', '', title)
    return title

def find_video_id_from_url(url):
    patterns = [r'^http://v.youku.com/v_show/id_([\w=]+).html',
                r'^http://player.youku.com/player.php/sid/([\w=]+)/v.swf',
                r'^loader\.swf\?VideoIDS=([\w=]+)',
                r'^([\w=]+)$']
    return r1_of(patterns, url)

def find_video_id_from_show_page(url):
    return re.search(r'<div class="btnplay">.*href="([^"]+)"', get_html(url)).group(1)

def youku_url(url):
    id = find_video_id_from_url(url)
    if id:
        return 'http://v.youku.com/v_show/id_%s.html' % id
    if re.match(r'http://www.youku.com/show_page/id_\w+.html', url):
        return find_video_id_from_show_page(url)
    if re.match(r'http://v.youku.com/v_playlist/\w+.html', url):
        return url
    return None

def parse_video_title(url, page):
    if re.search(r'v_playlist', url):
        # if we are playing a viedo from play list, the meta title might be incorrect
        title = r1_of([r'<div class="show_title" title="([^"]+)">[^<]', r'<title>([^<>]*)</title>'], page)
    else:
        title = r1_of([r'<div class="show_title" title="([^"]+)">[^<]', r'<meta name="title" content="([^"]*)"'], page)
    assert title
    title = trim_title(title)
    if re.search(r'v_playlist', url) and re.search(r'-.*\S+', title):
        title = re.sub(r'^[^-]+-\s*', '', title) # remove the special name from title for playlist video
    title = re.sub(r'—专辑：.*', '', title) # remove the special name from title for playlist video
    title = unescape_html(title)
    
    subtitle = re.search(r'<span class="subtitle" id="subtitle">([^<>]*)</span>', page)
    if subtitle:
        subtitle = subtitle.group(1).strip()
    if subtitle == title:
        subtitle = None
    if subtitle:
        title += '-' + subtitle
    return title

def parse_playlist_title(url, page):
    if re.search(r'v_playlist', url):
        # if we are playing a viedo from play list, the meta title might be incorrect
        title = re.search(r'<title>([^<>]*)</title>', page).group(1)
    else:
        title = re.search(r'<meta name="title" content="([^"]*)"', page).group(1)
    title = trim_title(title)
    if re.search(r'v_playlist', url) and re.search(r'-.*\S+', title):
        title = re.sub(r'^[^-]+-\s*', '', title)
    title = re.sub(r'^.*—专辑：《(.+)》', r'\1', title)
    title = unescape_html(title)
    return title

def parse_page(url):
    url = youku_url(url)
    page = get_html(url)
    id2 = re.search(r"var\s+videoId2\s*=\s*'(\S+)'", page).group(1)
    title = parse_video_title(url, page)
    return id2, title

def get_info(videoId2):
    return json.loads(get_html('http://v.youku.com/player/getPlayList/VideoIDS/' + videoId2))

def find_video(info, stream_type = None):
    #key = '%s%x' % (info['data'][0]['key2'], int(info['data'][0]['key1'], 16) ^ 0xA55AA5A5)
    segs = info['data'][0]['segs']
    types = segs.keys()
    if not stream_type:
        for x in ['hd2', 'mp4', 'flv']:
            if x in types:
                stream_type = x
                break
        else:
            raise NotImplementedError()
    assert stream_type in ('hd2', 'mp4', 'flv')
    file_type = {'hd2': 'flv', 'mp4': 'mp4', 'flv': 'flv'}[stream_type]
    
    seed = info['data'][0]['seed']
    source = list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ/\\:._-1234567890")
    mixed = ''
    while source:
        seed = (seed * 211 + 30031) & 0xFFFF
        index = seed * len(source) >> 16
        c = source.pop(index)
        mixed += c
    
    ids = info['data'][0]['streamfileids'][stream_type].split('*')[:-1]
    vid = ''.join(mixed[int(i)] for i in ids)
    
    sid = '%s%s%s' % (int(time() * 1000), randint(1000, 1999), randint(1000, 9999))
    
    urls = []
    for s in segs[stream_type]:
        no = '%02x' % int(s['no'])
        url = 'http://f.youku.com/player/getFlvPath/sid/%s_%s/st/%s/fileid/%s%s%s?K=%s&ts=%s' % (sid, no, file_type, vid[:8], no.upper(), vid[10:], s['k'], s['seconds'])
        urls.append((url, int(s['size'])))
    return urls

def file_type_of_url(url):
    return str(re.search(r'/st/([^/]+)/', url).group(1))

def youku_download_by_id(id2, title, output_dir = '.', stream_type = None, merge = True, info_only = False):
    info = get_info(id2)
    urls, sizes = zip(*find_video(info, stream_type))
    ext = file_type_of_url(urls[0])
    total_size = sum(sizes)
    
    urls = url_locations(urls) # Use real (redirected) URLs for resuming of downloads
    
    print_info(site_info, title, ext, total_size)
    if not info_only:
        download_urls(urls, title, ext, total_size, output_dir, merge = merge)

def youku_download(url, output_dir = '.', stream_type = None, merge = True, info_only = False):
    if not youku_url(url):
        youku_download_playlist(url, output_dir, merge, info_only)
        return
    
    id2, title = parse_page(url)
    title = title.replace('?', '-')
    
    youku_download_by_id(id2, title, output_dir, merge = merge, info_only = info_only)

def parse_playlist_videos(html):
    return re.findall(r'id="A_(\w+)"', html)

def parse_playlist_pages(html):
    m = re.search(r'<ul class="pages">.*?</ul>', html, flags = re.S)
    if m:
        urls = re.findall(r'href="([^"]+)"', m.group())
        x1, x2, x3 = re.match(r'^(.*page_)(\d+)(_.*)$', urls[-1]).groups()
        return ['http://v.youku.com%s%s%s?__rt=1&__ro=listShow' % (x1, i, x3) for i in range(2, int(x2) + 1)]
    else:
        return []

def parse_playlist(url):
    html = get_html(url)
    video_id = re.search(r"var\s+videoId\s*=\s*'(\d+)'", html).group(1)
    show_id = re.search(r'var\s+showid\s*=\s*"(\d+)"', html).group(1)
    list_url = 'http://v.youku.com/v_vpofficiallist/page_1_showid_%s_id_%s.html?__rt=1&__ro=listShow' % (show_id, video_id)
    html = get_html(list_url)
    ids = parse_playlist_videos(html)
    for url in parse_playlist_pages(html):
        ids.extend(parse_playlist_videos(get_html(url)))
    return ids

def parse_vplaylist(url):
    id = r1_of([r'^http://www.youku.com/playlist_show/id_(\d+)(?:_ascending_\d_mode_pic(?:_page_\d+)?)?.html',
                r'^http://v.youku.com/v_playlist/f(\d+)o[01]p\d+.html',
                r'^http://u.youku.com/user_playlist/pid_(\d+)_id_[\w=]+(?:_page_\d+)?.html'],
                url)
    assert id, 'not valid vplaylist url: ' + url
    url = 'http://www.youku.com/playlist_show/id_%s.html' % id
    n = int(re.search(r'<span class="num">(\d+)</span>', get_html(url)).group(1))
    return ['http://v.youku.com/v_playlist/f%so0p%s.html' % (id, i) for i in range(n)]

def youku_download_playlist(url, output_dir = '.', merge = True, info_only = False):
    if re.match(r'http://www.youku.com/show_page/id_\w+.html', url):
        url = find_video_id_from_show_page(url)
    
    if re.match(r'http://www.youku.com/playlist_show/id_\d+(?:_ascending_\d_mode_pic(?:_page_\d+)?)?.html', url):
        ids = parse_vplaylist(url)
    elif re.match(r'http://v.youku.com/v_playlist/f\d+o[01]p\d+.html', url):
        ids = parse_vplaylist(url)
    elif re.match(r'http://u.youku.com/user_playlist/pid_(\d+)_id_[\w=]+(?:_page_\d+)?.html', url):
        ids = parse_vplaylist(url)
    else:
        assert re.match(r'http://v.youku.com/v_show/id_([\w=]+).html', url), 'URL not supported as playlist'
        ids = parse_playlist(url)
    
    title = parse_playlist_title(url, get_html(url))
    title = title.replace('?', '-')
    output_dir = os.path.join(output_dir, title)
    
    for i, id in enumerate(ids):
        print('Processing %s of %s videos...' % (i + 1, len(ids)))
        youku_download(id, output_dir, merge = merge, info_only = info_only)

site_info = "Youku.com"
download = youku_download
download_playlist = youku_download_playlist
