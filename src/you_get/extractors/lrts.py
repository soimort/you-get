#!/usr/bin/env python

__all__ = ['lrts_download']

import logging
from ..common import *
from ..util import log, term

def lrts_download(url, output_dir='.', merge=True, info_only=False, **kwargs):
    html = get_html(url)
    args = kwargs.get('args')
    if not args: args = {}
    matched = re.search(r"/book/(\d+)", url)
    if not matched:
        raise AssertionError("not found book number: %s" % url)
    book_no = matched.group(1)
    book_title = book_no
    matched = re.search(r"<title>([^-]*)[-](.*)[,](.*)</title>", html)
    if matched:
        book_title = matched.group(1)

    matched = re.search(r"var totalCount='(\d+)'", html)
    if not matched:
        raise AssertionError("not found total count in html")
    total_count = int(matched.group(1))
    log.i('%s total: %s' % (book_title, total_count))
    first_page = 0
    if ('first' in args and args.first!= None):
        first_page = int(args.first)

    page_size = 10
    if ('page_size' in args and args.page_size != None):
        page_size = int(args.page_size)
    last_page = (total_count // page_size) + 1
    if ('last' in args and args.last != None):
        last_page = int(args.last)

    log.i('page size is %s, page from %s to %s' % (page_size, first_page, last_page))
    headers = {
      'Referer': url
    }
    items = []
    for page in range(first_page, last_page):
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
        if response_content['status'] == 'success' and response_content['data']:
            item['ok'] = True
            item['url'] = response_content['data']
            logging.debug('ok')

    items = list(filter(lambda i: 'ok' in i and i['ok'], items))
    log.i('Downloading %s: %s count ...' % (book_title, len(items)))

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
