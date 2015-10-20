#!/usr/bin/env python

__all__ = ['flickr_download']

from ..common import *

def flickr_download(url, output_dir='.', merge=True, info_only=False, **kwargs):
    page = get_html(url)
    title = match1(page, r'<meta property="og:title" content="([^"]*)"')
    photo_id = match1(page, r'"id":"([0-9]+)"')

    try: # extract video
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

    except: # extract images
        image = match1(page, r'<meta property="og:image" content="([^"]*)')
        ext = 'jpg'
        _, _, size = url_info(image)

        print_info(site_info, title, ext, size)
        if not info_only:
            download_urls([image], title, ext, size, output_dir, merge=merge)

site_info = "Flickr.com"
download = flickr_download
download_playlist = playlist_not_supported('flickr')
