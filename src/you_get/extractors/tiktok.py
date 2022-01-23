#!/usr/bin/env python

__all__ = ['tiktok_download']

from ..common import *

def tiktok_download(url, output_dir='.', merge=True, info_only=False, **kwargs):
    referUrl = url.split('?')[0]
    headers = fake_headers

    # trick or treat
    html = get_content(url, headers=headers)
    data = r1(r'<script id="__NEXT_DATA__".*?>(.*?)</script>', html)
    info = json.loads(data)
    wid = info['props']['initialProps']['$wid']
    cookie = 'tt_webid=%s; tt_webid_v2=%s' % (wid, wid)

    # here's the cookie
    headers['Cookie'] = cookie

    # try again
    html = get_content(url, headers=headers)
    data = r1(r'<script id="__NEXT_DATA__".*?>(.*?)</script>', html)
    info = json.loads(data)
    wid = info['props']['initialProps']['$wid']
    cookie = 'tt_webid=%s; tt_webid_v2=%s' % (wid, wid)

    videoData = info['props']['pageProps']['itemInfo']['itemStruct']
    videoId = videoData['id']
    videoUrl = videoData['video']['downloadAddr']
    uniqueId = videoData['author'].get('uniqueId')
    nickName = videoData['author'].get('nickname')

    title = '%s [%s]' % (nickName or uniqueId, videoId)

    # we also need the referer
    headers['Referer'] = referUrl

    mime, ext, size = url_info(videoUrl, headers=headers)

    print_info(site_info, title, mime, size)
    if not info_only:
        download_urls([videoUrl], title, ext, size, output_dir=output_dir, merge=merge, headers=headers)

site_info = "TikTok.com"
download = tiktok_download
download_playlist = playlist_not_supported('tiktok')
