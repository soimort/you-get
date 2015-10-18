#!/usr/bin/env python

__all__ = ['heavymusic_download']

from ..common import *

def heavymusic_download(url, output_dir='.', merge=True, info_only=False, **kwargs):
    html = get_html(url)
    tracks = re.findall(r'href="(online2\.php[^"]+)"', html)
    for track in tracks:
        band = r1(r'band=([^&]*)', track)
        album = r1(r'album=([^&]*)', track)
        title = r1(r'track=([^&]*)', track)
        file_url = 'http://www.heavy-music.ru/online2.php?band=%s&album=%s&track=%s' % (parse.quote(band), parse.quote(album), parse.quote(title))
        _, _, size = url_info(file_url)

        print_info(site_info, title, 'mp3', size)
        if not info_only:
            download_urls([file_url], title[:-4], 'mp3', size, output_dir, merge=merge)

site_info = "heavy-music.ru"
download = heavymusic_download
download_playlist = heavymusic_download
