#!/usr/bin/env python

__all__ = ['tiktok_download']

from ..common import *

def tiktok_download(url, output_dir='.', merge=True, info_only=False, **kwargs):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0',
        'Accept-Encoding': 'gzip, deflate',
        'Accept': '*/*',
        'Referer': 'https://www.tiktok.com/',
        'Connection': 'keep-alive'  # important
    }

    m = re.match('(https?://)?([^/]+)(/.*)', url)
    host = m.group(2)
    if host != 'www.tiktok.com':  # non-canonical URL
        if host == 'vt.tiktok.com':  # short URL
            url = get_location(url)
        vid = r1(r'/video/(\d+)', url)
        url = 'https://www.tiktok.com/@/video/%s/' % vid
        host = 'www.tiktok.com'
    else:
        url = m.group(3).split('?')[0]
        vid = url.split('/')[3]  # should be a string of numbers

    html, set_cookie = getHttps(host, url, headers=headers)
    tt_chain_token = r1('tt_chain_token=([^;]+);', set_cookie)
    headers['Cookie'] = 'tt_chain_token=%s' % tt_chain_token

    data = r1(r'<script id="__UNIVERSAL_DATA_FOR_REHYDRATION__" type="application/json">(.*?)</script>', html)
    info = json.loads(data)
    itemStruct = info['__DEFAULT_SCOPE__']['webapp.video-detail']['itemInfo']['itemStruct']
    downloadAddr = itemStruct['video']['downloadAddr']
    author = itemStruct['author']['uniqueId']
    nickname = itemStruct['author']['nickname']
    title = '%s [%s]' % (nickname or author, vid)

    mime, ext, size = url_info(downloadAddr, headers=headers)

    print_info(site_info, title, mime, size)
    if not info_only:
        download_urls([downloadAddr], title, ext, size, output_dir=output_dir, merge=merge, headers=headers)

site_info = "TikTok.com"
download = tiktok_download
download_playlist = playlist_not_supported('tiktok')
