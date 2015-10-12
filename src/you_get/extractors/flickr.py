#!/usr/bin/env python

__all__ = ['flickr_download']

from ..common import *

def flickr_download(url, output_dir='.', merge=True, info_only=False, **kwargs):
    html = get_html(url)
    title = match1(html, r'<meta property="og:title" content="([^"]*)"')
    photo_id = match1(html, r'"id":"([0-9]+)"')

    html = get_html('https://secure.flickr.com/apps/video/video_mtl_xml.gne?photo_id=%s' % photo_id)
    node_id = match1(html, r'<Item id="id">(.+)</Item>')
    secret = match1(html, r'<Item id="photo_secret">(.+)</Item>')

    html = get_html('https://secure.flickr.com/video_playlist.gne?node_id=%s&secret=%s' % (node_id, secret))
    app = match1(html, r'APP="([^"]+)"')
    fullpath = unescape_html(match1(html, r'FULLPATH="([^"]+)"'))
    url = app + fullpath

    mime, ext, size = url_info(url)

    print_info(site_info, title, mime, size)
    if not info_only:
        download_urls([url], title, ext, size, output_dir, merge=merge, faker=True)

site_info = "Flickr.com"
download = flickr_download
download_playlist = playlist_not_supported('flickr')
