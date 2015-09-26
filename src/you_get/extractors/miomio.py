#!/usr/bin/env python

__all__ = ['miomio_download']

from ..common import *

from .sina import sina_download_by_xml
from .tudou import tudou_download_by_id
from .youku import youku_download_by_vid

def miomio_download(url, output_dir = '.', merge = True, info_only = False, **kwargs):
    html = get_html(url)

    title = r1(r'<meta name="description" content="([^"]*)"', html)
    flashvars = r1(r'flashvars="(type=[^"]*)"', html)

    t = r1(r'type=(\w+)', flashvars)
    id = r1(r'vid=([^"]+)', flashvars)
    if t == 'youku':
        youku_download_by_vid(id, title=title, output_dir=output_dir, merge=merge, info_only=info_only)
    elif t == 'tudou':
        tudou_download_by_id(id, title, output_dir=output_dir, merge=merge, info_only=info_only)
    elif t == 'sina' or t=='video':
        url = "http://www.miomio.tv/mioplayer/mioplayerconfigfiles/sina.php?vid=" + id
        xml = get_content (url, headers=fake_headers, decoded=True)
        sina_download_by_xml(xml, title, output_dir=output_dir, merge=merge, info_only=info_only)
    else:
        raise NotImplementedError(flashvars)

site_info = "MioMio.tv"
download = miomio_download
download_playlist = playlist_not_supported('miomio')
