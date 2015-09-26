#!/usr/bin/env python

__all__ = ['qq_download']

from ..common import *

def qq_download_by_vid(vid, title, output_dir='.', merge=True, info_only=False):
    api = "http://vv.video.qq.com/geturl?otype=json&vid=%s" % vid
    content = get_html(api)
    output_json = json.loads(match1(content, r'QZOutputJson=(.*)')[:-1])
    url = output_json['vd']['vi'][0]['url']
    _, ext, size = url_info(url, faker=True)

    print_info(site_info, title, ext, size)
    if not info_only:
        download_urls([url], title, ext, size, output_dir=output_dir, merge=merge)

def qq_download(url, output_dir='.', merge=True, info_only=False, **kwargs):
    content = get_html(url)
    vid = match1(content, r'vid\s*:\s*"\s*([^"]+)"')
    title = match1(content, r'title\s*:\s*"\s*([^"]+)"')

    qq_download_by_vid(vid, title, output_dir, merge, info_only)

site_info = "QQ.com"
download = qq_download
download_playlist = playlist_not_supported('qq')
