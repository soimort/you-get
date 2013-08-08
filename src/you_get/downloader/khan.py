#!/usr/bin/env python

__all__ = ['khan_download']

from ..common import *
from .youtube import youtube_download_by_id

def khan_download(url, output_dir = '.', merge = True, info_only = False):
    page = get_html(url)
    id = page[page.find('src="https://www.youtube.com/embed/') + len('src="https://www.youtube.com/embed/') :page.find('?enablejsapi=1&wmode=transparent&modestbranding=1&rel=0&fs=1&showinfo=0')]
    youtube_download_by_id(id, output_dir=output_dir, merge=merge, info_only=info_only)

site_info = "khanacademy.org"
download = khan_download
download_playlist = playlist_not_supported('khan')
