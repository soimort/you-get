#!/usr/bin/env python

__all__ = ['vine_download']

from ..common import *
import json


def vine_download(url, output_dir='.', merge=True, info_only=False, **kwargs):
    html = get_content(url)

    video_id = r1(r'vine.co/v/([^/]+)', url)
    title = r1(r'<title>([^<]*)</title>', html)
    stream = r1(r'<meta property="twitter:player:stream" content="([^"]*)">', html)
    if not stream:  # https://vine.co/v/.../card
        stream = r1(r'"videoUrl":"([^"]+)"', html)
        if stream:
            stream = stream.replace('\\/', '/')
        else:
            posts_url = 'https://archive.vine.co/posts/' + video_id + '.json'
            json_data = json.loads(get_content(posts_url))
            stream = json_data['videoDashUrl']
            title = json_data['description']
            if title == "":
                title = json_data['username'].replace(" ", "_") + "_" + video_id

    mime, ext, size = url_info(stream)

    print_info(site_info, title, mime, size)
    if not info_only:
        download_urls([stream], title, ext, size, output_dir, merge=merge)


site_info = "Vine.co"
download = vine_download
download_playlist = playlist_not_supported('vine')
