#!/usr/bin/env python

__all__ = ['yinyuetai_download', 'yinyuetai_download_by_id']

from ..common import *

def yinyuetai_download_by_id(id, title = None, output_dir = '.', merge = True, info_only = False):
    assert title
    html = get_html('http://www.yinyuetai.com/insite/get-video-info?flex=true&videoId=' + id)

    for quality in ['he\w*', 'hd\w*', 'hc\w*', '\w+']:
        url = r1(r'(http://' + quality + '\.yinyuetai\.com/uploads/videos/common/\w+\.(?:flv|mp4)\?(?:sc=[a-f0-9]{16}|v=\d{12}))', html)
        if url:
            break
    assert url
    type = ext = r1(r'\.(flv|mp4)', url)
    _, _, size = url_info(url)

    print_info(site_info, title, type, size)
    if not info_only:
        download_urls([url], title, ext, size, output_dir, merge = merge)

def yinyuetai_download(url, output_dir = '.', merge = True, info_only = False):
    id = r1(r'http://\w+.yinyuetai.com/video/(\d+)$', url.split('?')[0])
    assert id
    html = get_html(url, 'utf-8')
    title = r1(r'<meta property="og:title"\s+content="([^"]+)"/>', html)
    assert title
    title = parse.unquote(title)
    title = escape_file_path(title)
    yinyuetai_download_by_id(id, title, output_dir, merge = merge, info_only = info_only)

site_info = "YinYueTai.com"
download = yinyuetai_download
download_playlist = playlist_not_supported('yinyuetai')
