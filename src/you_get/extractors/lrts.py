#!/usr/bin/env python

__all__ = ['lrts_download']

import logging
from ..common import *

def lrts_download(url, output_dir='.', merge=True, info_only=False, **kwargs):
    html = get_html(url)
    matched = re.search(r"/book/(\d+)", url)
    if not matched:
        raise AssertionError("not found book number: %s" % url)
    book_no = matched.group(1)
    book_title = book_no
    matched = re.search(r"<title>(.*)-(.*)</title>", html)
    if matched:
        book_title = matched.group(1)

    matched = re.search(r"var totalCount='(\d+)'", html)
    if not matched:
        raise AssertionError("not found total count in html")
    total_count = int(matched.group(1))
    logging.debug('total: %s' % total_count)
    page_size = 10
    logging.debug('total page count: %s' % ((total_count // page_size) + 1))
    headers = {
      'Referer': url
    }
    items = []
    if (total_count > page_size):
        for page in range((total_count // page_size) + 1):
            page_url = 'http://www.lrts.me/ajax/book/%s/%s/%s' % (book_no, page, page_size)
            response_content = json.loads(post_content(page_url, headers))
            if response_content['status'] != 'success':
                raise AssertionError("got the page failed: %s" % (page_url))
            data = response_content['data']['data']
            if data:
                for i in data:
                    i['resName'] = parse.unquote(i['resName'])
                items.extend(data)
            else:
                break

    headers = {
      'Referer': 'http://www.lrts.me/playlist'
    }

    for item in items:
        i_url = 'http://www.lrts.me/ajax/path/4/%s/%s' % (item['fatherResId'], item['resId'])
        response_content = json.loads(post_content(i_url, headers))
        # logging.debug(response_content)
        if response_content['status'] == 'success' and response_content['data']:
            item['ok'] = True
            item['url'] = response_content['data']

    items = list(filter(lambda i: 'ok' in i and i['ok'], items))
    print('Downloading %s: %s count ...' % (book_title, len(items)))

    for item in items:
        title = item['resName']
        file_url = item['url']
        # if not file_url: continue
        _, _, size = url_info(file_url)
        print_info(site_info, title, 'mp3', size)
        if not info_only:
            download_urls([file_url], title, 'mp3', size, output_dir, merge=merge)

site_info = "lrts.me"
download = lrts_download
download_playlist = lrts_download
