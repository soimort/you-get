#!/usr/bin/env python

__all__ = ['dailymotion_download']

from ..common import *
import urllib.parse

def rebuilt_url(url):
    path = urllib.parse.urlparse(url).path
    aid = path.split('/')[-1].split('_')[0]
    return 'http://www.dailymotion.com/embed/video/{}?autoplay=1'.format(aid)

def dailymotion_download(url, output_dir='.', merge=True, info_only=False, **kwargs):
    """Downloads Dailymotion videos by URL.
    """

    html = get_content(rebuilt_url(url))
    info = json.loads(match1(html, r'qualities":({.+?}),"'))
    title = match1(html, r'"video_title"\s*:\s*"([^"]+)"') or \
            match1(html, r'"title"\s*:\s*"([^"]+)"')
    title = unicodize(title)

    for quality in ['1080','720','480','380','240','144','auto']:
        try:
            real_url = info[quality][1]["url"]
            if real_url:
                break
        except KeyError:
            pass

    mime, ext, size = url_info(real_url)

    print_info(site_info, title, mime, size)
    if not info_only:
        download_urls([real_url], title, ext, size, output_dir=output_dir, merge=merge)

site_info = "Dailymotion.com"
download = dailymotion_download
download_playlist = playlist_not_supported('dailymotion')
