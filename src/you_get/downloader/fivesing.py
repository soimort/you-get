#!/usr/bin/env python

__all__ = ['fivesing_download']

from ..common import *

def fivesing_download(url, output_dir=".", merge=True, info_only=False):
    html = get_html(url)
    title = r1(r'var SongName   = "(.*)";', html)
    url = r1(r'file: "(\S*)"', html)
    songtype, ext, size = url_info(url)
    print_info(site_info, title, songtype, size)
    if not info_only:
        download_urls([url], title, ext, size, output_dir)

site_info = "5sing.com"
download = fivesing_download
download_playlist = playlist_not_supported("5sing")
