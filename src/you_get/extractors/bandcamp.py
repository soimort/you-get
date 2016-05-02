#!/usr/bin/env python

__all__ = ['bandcamp_download']

from ..common import *

def bandcamp_download(url, output_dir='.', merge=True, info_only=False, **kwargs):
    html = get_html(url)
    trackinfo = json.loads(r1(r'(\[{"(video_poster_url|video_caption)".*}\]),', html))
    for track in trackinfo:
        track_num = track['track_num']
        title = '%s. %s' % (track_num, track['title'])
        file_url = 'http:' + track['file']['mp3-128']
        mime, ext, size = url_info(file_url)

        print_info(site_info, title, mime, size)
        if not info_only:
            download_urls([file_url], title, ext, size, output_dir, merge=merge)

site_info = "Bandcamp.com"
download = bandcamp_download
download_playlist = bandcamp_download
