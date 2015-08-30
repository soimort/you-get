#!/usr/bin/env python

__all__ = ['video_178_download']

from ..common import *

from .youku import youku_download_by_vid

def video_178_download(url, output_dir = '.', merge = True, info_only = False):
    html = get_html(url)
    title = match1(html, "<title>([^<>]+)</title>")
    vid = match1(html, "http://player.youku.com/embed/([a-zA-Z0-9=]+)")
    youku_download_by_vid(vid, title=title, output_dir=output_dir, merge=merge, info_only=info_only)


site_info = "178.com"
download = video_178_download
download_playlist = playlist_not_supported('178')
