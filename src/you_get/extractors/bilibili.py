#!/usr/bin/env python

__all__ = ['bilibili_download']

import json
import re
from ..common import *

def get_srt_xml(cid):
    return get_html('http://comment.bilibili.com/%s.xml' % cid)

def bilibili_download_by_api(url, output_dir='.', merge=True, info_only=False, **kwargs):
    title = r1(r'cid=(\d+)', url)
    info = json.loads(get_content(url))
    urls = [i['url'] for i in info['durl']]

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

def bilibili_download(url, output_dir='.', merge=True, info_only=False, **kwargs):
    if re.match(r'https?://interface\.bilibili\.com/', url):
        # quick hack for explicit API
        bilibili_download_by_api(url, output_dir=output_dir, merge=merge, info_only=info_only, **kwargs)
        return

    if re.match(r'https?://bangumi\.bilibili\.com/', url):
        # quick hack for bangumi URLs
        html = get_content(url)
        url = r1(r'"([^"]+)" class="v-av-link"', html)

    html = get_content(url)
    main_title = r1_of([r'<meta name="title" content="\s*([^<>]{1,999})\s*" />',
                        r'<h1[^>]*>\s*([^<>]+)\s*</h1>'], html)
    cid = r1(r'cid=(\d+)', html)

    aid = r1(r'av(\d+)', url)
    page = r1(r'index_(\d+)', url)
    sub_titles = re.findall('<option value=.*>\s*([^<>]+)\s*</option>', html)
    if page is None and sub_titles: # download all
        for t in enumerate(sub_titles):
            page, sub_title = t[0] + 1, t[1]
            title = main_title + ' - ' + sub_title

            api = 'http://www.bilibili.com/m/html5?aid=%s&page=%s' % (aid, page)
            info = json.loads(get_content(api))
            src = info['src']
            _, type_, size = url_info(src)
            print_info(site_info, title, type_, size)
            if not info_only:
                download_urls([src], title, type_, total_size=size, output_dir=output_dir, merge=merge)

    else: # download selected
        if page is None: page = 1
        sub_title = r1('<option value=.* selected>\s*([^<>]+)\s*</option>', html)
        if sub_title is None:
            sub_title = r1('<option value=.*>\s*([^<>]+)\s*</option>', html)
        if sub_title:
            title = main_title + ' - ' + sub_title
        else:
            title = main_title

        api = 'http://www.bilibili.com/m/html5?aid=%s&page=%s' % (aid, page)
        info = json.loads(get_content(api))
        src = info['src']
        _, type_, size = url_info(src)
        print_info(site_info, title, type_, size)
        if not info_only:
            download_urls([src], title, type_, total_size=size, output_dir=output_dir, merge=merge)

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
