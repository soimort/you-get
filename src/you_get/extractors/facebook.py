#!/usr/bin/env python

__all__ = ['facebook_download']

from ..common import *
import json


def facebook_download(url, output_dir='.', merge=True, info_only=False, **kwargs):
    html = get_html(url)

    title = r1(r'<title id="pageTitle">(.+) \| Facebook</title>', html)
    s2 = parse.unquote(unicodize(r1(r'\["params","([^"]*)"\]', html)))
    data = json.loads(s2)
    video_data = data["video_data"]["progressive"]
    for fmt in ["hd_src", "sd_src"]:
        src = video_data[0][fmt]
        if src:
            break

    type, ext, size = url_info(src, True)

    print_info(site_info, title, type, size)
    if not info_only:
        download_urls([src], title, ext, size, output_dir, merge=merge)

site_info = "Facebook.com"
download = facebook_download
download_playlist = playlist_not_supported('facebook')
