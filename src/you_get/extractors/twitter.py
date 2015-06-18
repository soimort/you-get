#!/usr/bin/env python

__all__ = ['twitter_download']

from ..common import *

def twitter_download(url, output_dir='.', merge=True, info_only=False):
    html = get_html(url)
    screen_name = r1(r'data-screen-name="([^"]*)"', html)
    item_id = r1(r'data-item-id="([^"]*)"', html)
    title = "{} [{}]".format(screen_name, item_id)
    icards = r1(r'data-src="([^"]*)"', html)
    if icards:
        html = get_html("https://twitter.com" + icards)
        data = json.loads(unescape_html(r1(r'data-player-config="([^"]*)"', html)))
        source = data['playlist'][0]['source']
    else:
        source = r1(r'<source video-src="([^"]*)"', html)
    mime, ext, size = url_info(source)

    print_info(site_info, title, mime, size)
    if not info_only:
        download_urls([source], title, ext, size, output_dir, merge=merge)

site_info = "Twitter.com"
download = twitter_download
download_playlist = playlist_not_supported('twitter')
