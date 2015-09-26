#!/usr/bin/env python

__all__ = ['bilibili_download']

from ..common import *

from .sina import sina_download_by_vid
from .tudou import tudou_download_by_id
from .youku import youku_download_by_vid

import hashlib
import re

# API key provided by cnbeining
appkey='85eb6835b0a1034e';
secretkey = '2ad42749773c441109bdc0191257a664'
client = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'UTF-8,*;q=0.5',
    'Accept-Encoding': 'gzip,deflate,sdch',
    'Accept-Language': 'en-US,en;q=0.8',
    #'User-Agent': 'Biligrab /0.8 (cnbeining@gmail.com)'
    'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.94 Safari/537.36"
}

def get_srt_xml(id):
    url = 'http://comment.bilibili.com/%s.xml' % id
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
    try:
        doc = parseString(xml.encode('utf-8'))
        urls = [durl.getElementsByTagName('url')[0].firstChild.nodeValue for durl in doc.getElementsByTagName('durl')]
        return urls
    except:
        return []

def bilibili_download_by_cids(cids, title, output_dir='.', merge=True, info_only=False):
    urls = []
    for cid in cids:
        sign_this = hashlib.md5(bytes('appkey=' + appkey + '&cid=' + cid + secretkey, 'utf-8')).hexdigest()
        url = 'http://interface.bilibili.com/playurl?appkey=' + appkey + '&cid=' + cid + '&sign=' + sign_this
        urls += [i
                if not re.match(r'.*\.qqvideo\.tc\.qq\.com', i)
                else re.sub(r'.*\.qqvideo\.tc\.qq\.com', 'http://vsrc.store.qq.com', i)
                for i in parse_cid_playurl(get_content(url, headers=client))]

    type_ = ''
    size = 0
    for url in urls:
        _, type_, temp = url_info(url)
        size += temp

    print_info(site_info, title, type_, size)
    if not info_only:
        download_urls(urls, title, type_, total_size=None, output_dir=output_dir, merge=merge)

def bilibili_download_by_cid(id, title, output_dir='.', merge=True, info_only=False):
    sign_this = hashlib.md5(bytes('appkey=' + appkey + '&cid=' + id + secretkey, 'utf-8')).hexdigest()
    url = 'http://interface.bilibili.com/playurl?appkey=' + appkey + '&cid=' + id + '&sign=' + sign_this
    urls = [i
            if not re.match(r'.*\.qqvideo\.tc\.qq\.com', i)
            else re.sub(r'.*\.qqvideo\.tc\.qq\.com', 'http://vsrc.store.qq.com', i)
            for i in parse_cid_playurl(get_content(url, headers=client))]

    type_ = ''
    size = 0
    for url in urls:
        _, type_, temp = url_info(url)
        size += temp or 0

    print_info(site_info, title, type_, size)
    if not info_only:
        download_urls(urls, title, type_, total_size=None, output_dir=output_dir, merge=merge)

def bilibili_download(url, output_dir='.', merge=True, info_only=False, **kwargs):
    html = get_html(url)

    title = r1_of([r'<meta name="title" content="([^<>]{1,999})" />',r'<h1[^>]*>([^<>]+)</h1>'], html)
    title = unescape_html(title)
    title = escape_file_path(title)

    flashvars = r1_of([r'(cid=\d+)', r'(cid: \d+)', r'flashvars="([^"]+)"', r'"https://[a-z]+\.bilibili\.com/secure,(cid=\d+)(?:&aid=\d+)?"'], html)
    assert flashvars
    flashvars = flashvars.replace(': ','=')
    t, id = flashvars.split('=', 1)
    id = id.split('&')[0]
    if t == 'cid':
        # Multi-P
        cids = []
        p = re.findall('<option value=\'([^\']*)\'>', html)
        if not p:
            bilibili_download_by_cid(id, title, output_dir=output_dir, merge=merge, info_only=info_only)
        else:
            for i in p:
                html = get_html("http://www.bilibili.com%s" % i)
                flashvars = r1_of([r'(cid=\d+)', r'flashvars="([^"]+)"', r'"https://[a-z]+\.bilibili\.com/secure,(cid=\d+)(?:&aid=\d+)?"'], html)
                if flashvars:
                    t, cid = flashvars.split('=', 1)
                    cids.append(cid.split('&')[0])
            bilibili_download_by_cids(cids, title, output_dir=output_dir, merge=merge, info_only=info_only)

    elif t == 'vid':
        sina_download_by_vid(id, title, output_dir = output_dir, merge = merge, info_only = info_only)
    elif t == 'ykid':
        youku_download_by_vid(id, title=title, output_dir = output_dir, merge = merge, info_only = info_only)
    elif t == 'uid':
        tudou_download_by_id(id, title, output_dir = output_dir, merge = merge, info_only = info_only)
    else:
        raise NotImplementedError(flashvars)

    if not info_only:
        title = get_filename(title)
        print('Downloading %s ...\n' % (title + '.cmt.xml'))
        xml = get_srt_xml(id)
        with open(os.path.join(output_dir, title + '.cmt.xml'), 'w', encoding='utf-8') as x:
            x.write(xml)

site_info = "bilibili.com"
download = bilibili_download
download_playlist = playlist_not_supported('bilibili')
