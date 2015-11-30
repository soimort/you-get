#!/usr/bin/env python

__all__ = ['khan_download']

from ..common import *
from .youtube import YouTube

def khan_download(url, output_dir='.', merge=True, info_only=False, **kwargs):
    html = get_content(url)
    youtube_url = re.search('<meta property="og:video" content="([^"]+)', html).group(1)
    YouTube().download_by_url(youtube_url, output_dir=output_dir, merge=merge, info_only=info_only)

site_info = "khanacademy.org"
download = khan_download
download_playlist = playlist_not_supported('khan')
