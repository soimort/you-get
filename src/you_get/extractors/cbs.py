#!/usr/bin/env python

__all__ = ['cbs_download']

from ..common import *

from .theplatform import theplatform_download_by_pid

def cbs_download(url, output_dir='.', merge=True, info_only=False, **kwargs):
    """Downloads CBS videos by URL.
    """

    html = get_content(url)
    pid = match1(html, r'video\.settings\.pid\s*=\s*\'([^\']+)\'')
    title = match1(html, r'video\.settings\.title\s*=\s*\"([^\"]+)\"')

    theplatform_download_by_pid(pid, title, output_dir=output_dir, merge=merge, info_only=info_only)

site_info = "CBS.com"
download = cbs_download
download_playlist = playlist_not_supported('cbs')
