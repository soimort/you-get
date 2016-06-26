#!/usr/bin/env python

__all__ = ['bilibili_download']

from ..common import *

from .sina import sina_download_by_vid
from .tudou import tudou_download_by_id
from .youku import youku_download_by_vid

import hashlib
import re

appkey = 'f3bb208b3d081dc8'


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
        url = 'http://interface.bilibili.com/playurl?appkey=' + appkey + '&cid=' + cid
        urls += [i
                 if not re.match(r'.*\.qqvideo\.tc\.qq\.com', i)
                 else re.sub(r'.*\.qqvideo\.tc\.qq\.com', 'http://vsrc.store.qq.com', i)
                 for i in parse_cid_playurl(get_content(url))]

    type_ = ''
    size = 0
    for url in urls:
        _, type_, temp = url_info(url)
        size += temp

    print_info(site_info, title, type_, size)
    if not info_only:
        download_urls(urls, title, type_, total_size=None, output_dir=output_dir, merge=merge)


def bilibili_download_by_cid(cid, title, output_dir='.', merge=True, info_only=False):
    url = 'http://interface.bilibili.com/playurl?appkey=' + appkey + '&cid=' + cid
    urls = [i
            if not re.match(r'.*\.qqvideo\.tc\.qq\.com', i)
            else re.sub(r'.*\.qqvideo\.tc\.qq\.com', 'http://vsrc.store.qq.com', i)
            for i in parse_cid_playurl(get_content(url))]

    type_ = ''
    size = 0
    try:
        for url in urls:
            _, type_, temp = url_info(url)
            size += temp or 0
    except error.URLError:
        log.wtf('[Failed] DNS not resolved. Please change your DNS server settings.')

    print_info(site_info, title, type_, size)
    if not info_only:
        download_urls(urls, title, type_, total_size=None, output_dir=output_dir, merge=merge)


def bilibili_live_download_by_cid(cid, title, output_dir='.', merge=True, info_only=False):
    api_url = 'http://live.bilibili.com/api/playurl?cid=' + cid
    urls = parse_cid_playurl(get_content(api_url))

    for url in urls:
        _, type_, _ = url_info(url)
        size = 0
        print_info(site_info, title, type_, size)
        if not info_only:
            download_urls([url], title, type_, total_size=None, output_dir=output_dir, merge=merge)


def bilibili_download(url, output_dir='.', merge=True, info_only=False, **kwargs):
    html = get_content(url)

    if re.match(r'https?://bangumi\.bilibili\.com/', url):
        # quick hack for bangumi URLs
        url = r1(r'"([^"]+)" class="v-av-link"', html)
        html = get_content(url)

    title = r1_of([r'<meta name="title" content="([^<>]{1,999})" />',
                   r'<h1[^>]*>([^<>]+)</h1>'], html)
    if title:
        title = unescape_html(title)
        title = escape_file_path(title)

    flashvars = r1_of([r'(cid=\d+)', r'(cid: \d+)', r'flashvars="([^"]+)"',
                       r'"https://[a-z]+\.bilibili\.com/secure,(cid=\d+)(?:&aid=\d+)?"'], html)
    assert flashvars
    flashvars = flashvars.replace(': ', '=')
    t, cid = flashvars.split('=', 1)
    cid = cid.split('&')[0]
    if t == 'cid':
        if re.match(r'https?://live\.bilibili\.com/', url):
            title = r1(r'<title>([^<>]+)</title>', html)
            bilibili_live_download_by_cid(cid, title, output_dir=output_dir, merge=merge, info_only=info_only)

        else:
            # multi-P
            cids = []
            pages = re.findall('<option value=\'([^\']*)\'', html)
            titles = re.findall('<option value=.*>(.+)</option>', html)
            for i, page in enumerate(pages):
                html = get_html("http://www.bilibili.com%s" % page)
                flashvars = r1_of([r'(cid=\d+)',
                                   r'flashvars="([^"]+)"',
                                   r'"https://[a-z]+\.bilibili\.com/secure,(cid=\d+)(?:&aid=\d+)?"'], html)
                if flashvars:
                    t, cid = flashvars.split('=', 1)
                    cids.append(cid.split('&')[0])
                if url.endswith(page):
                    cids = [cid.split('&')[0]]
                    titles = [titles[i]]
                    break

            # no multi-P
            if not pages:
                cids = [cid]
                titles = [r1(r'<option value=.* selected>(.+)</option>', html) or title]

            for i in range(len(cids)):
                bilibili_download_by_cid(cids[i],
                                         titles[i],
                                         output_dir=output_dir,
                                         merge=merge,
                                         info_only=info_only)

    elif t == 'vid':
        sina_download_by_vid(cid, title=title, output_dir=output_dir, merge=merge, info_only=info_only)
    elif t == 'ykid':
        youku_download_by_vid(cid, title=title, output_dir=output_dir, merge=merge, info_only=info_only)
    elif t == 'uid':
        tudou_download_by_id(cid, title, output_dir=output_dir, merge=merge, info_only=info_only)
    else:
        raise NotImplementedError(flashvars)

    if not info_only and not dry_run:
        if not kwargs['caption']:
            print('Skipping danmaku.')
            return
        title = get_filename(title)
        print('Downloading %s ...\n' % (title + '.cmt.xml'))
        xml = get_srt_xml(cid)
        with open(os.path.join(output_dir, title + '.cmt.xml'), 'w', encoding='utf-8') as x:
            x.write(xml)


site_info = "bilibili.com"
download = bilibili_download
download_playlist = bilibili_download
