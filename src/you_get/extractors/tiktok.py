#!/usr/bin/env python

__all__ = ['tiktok_download']

from ..common import *

def tiktok_download(url, output_dir='.', merge=True, info_only=False, **kwargs):
    html = get_html(url, faker=True)

    data = r1(r'<script id="__NEXT_DATA__".*?>(.*?)</script>', html)
    info = json.loads(data)
    videoData = info['props']['pageProps']['videoData']
    urls = videoData['itemInfos']['video']['urls']
    videoId = videoData['itemInfos']['id']
    uniqueId = videoData['authorInfos'].get('uniqueId')
    nickName = videoData['authorInfos'].get('nickName')

    for i, videoUrl in enumerate(urls):
        title = '%s [%s]' % (nickName or uniqueId, videoId)
        if len(urls) > 1:
            title = '%s [%s]' % (title, i)

        mime, ext, size = url_info(videoUrl, headers={'Referer': url})

        print_info(site_info, title, mime, size)
        if not info_only:
            download_urls([videoUrl], title, ext, size, output_dir=output_dir, merge=merge, headers={'Referer': url})

site_info = "TikTok.com"
download = tiktok_download
download_playlist = playlist_not_supported('tiktok')
