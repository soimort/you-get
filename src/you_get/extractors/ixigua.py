#!/usr/bin/env python
__all__ = ['ixigua_download']

from .toutiao import download as toutiao_download
from .toutiao import download_playlist as toutiao_download_playlist


def ixigua_download(url, output_dir='.', merge=True, info_only=False, **kwargs):
    return toutiao_download(url.replace('ixigua', '365yg'))


site_info = "ixigua.com"
download = ixigua_download
download_playlist = toutiao_download_playlist
