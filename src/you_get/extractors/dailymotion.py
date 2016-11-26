#!/usr/bin/env python

__all__ = ['dailymotion_download']

from ..common import *

def extract_m3u(url):
    content = get_content(url)
    m3u_url = re.findall(r'http://.*', content)[0]
    return match1(m3u_url, r'([^#]+)')

def dailymotion_download(url, output_dir = '.', merge = True, info_only = False, **kwargs):
    """Downloads Dailymotion videos by URL.
    """

    html = get_content(url)
    info = json.loads(match1(html, r'qualities":({.+?}),"'))
    title = match1(html, r'"video_title"\s*:\s*"([^"]+)"') or \
            match1(html, r'"title"\s*:\s*"([^"]+)"')

    for quality in ['1080','720','480','380','240','auto']:
        try:
            real_url = info[quality][0]["url"]
            if real_url:
                break
        except KeyError:
            pass

    m3u_url = extract_m3u(real_url)
    mime, ext, size = 'video/mp4', 'mp4', 0

    print_info(site_info, title, mime, size)
    if not info_only:
        download_url_ffmpeg(m3u_url, title, ext, output_dir=output_dir, merge=merge)

site_info = "Dailymotion.com"
download = dailymotion_download
download_playlist = playlist_not_supported('dailymotion')
