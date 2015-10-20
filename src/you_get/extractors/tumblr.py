#!/usr/bin/env python

__all__ = ['tumblr_download']

from ..common import *

import re

def tumblr_download(url, output_dir='.', merge=True, info_only=False, **kwargs):
    html = parse.unquote(get_html(url)).replace('\/', '/')
    feed = r1(r'<meta property="og:type" content="tumblr-feed:(\w+)" />', html)

    if feed in ['photo', 'photoset'] or feed is None:
        page_title = r1(r'<meta name="description" content="([^"\n]+)', html) or \
                     r1(r'<meta property="og:description" content="([^"\n]+)', html) or \
                     r1(r'<title>([^<\n]*)', html)
        urls = re.findall(r'(https?://[^;"]+/tumblr_[^;"]+_\d+\.jpg)', html) +\
               re.findall(r'(https?://[^;"]+/tumblr_[^;"]+_\d+\.png)', html) +\
               re.findall(r'(https?://[^;"]+/tumblr_[^";]+_\d+\.gif)', html)

        tuggles = {}
        for url in urls:
            filename = parse.unquote(url.split('/')[-1])
            title = '.'.join(filename.split('.')[:-1])
            tumblr_id = r1(r'^tumblr_(.+)_\d+$', title)
            quality = int(r1(r'^tumblr_.+_(\d+)$', title))
            ext = filename.split('.')[-1]
            size = int(get_head(url)['Content-Length'])
            if tumblr_id not in tuggles or tuggles[tumblr_id]['quality'] < quality:
                tuggles[tumblr_id] = {
                    'title': title,
                    'url': url,
                    'quality': quality,
                    'ext': ext,
                    'size': size,
                }

        size = sum([tuggles[t]['size'] for t in tuggles])
        print_info(site_info, page_title, None, size)

        if not info_only:
            for t in tuggles:
                title = tuggles[t]['title']
                ext = tuggles[t]['ext']
                size = tuggles[t]['size']
                url = tuggles[t]['url']
                print_info(site_info, title, ext, size)
                download_urls([url], title, ext, size,
                              output_dir=output_dir)
        return

    elif feed == 'audio':
        real_url = r1(r'source src=\\x22([^\\]+)\\', html)
        if not real_url:
            real_url = r1(r'audio_file=([^&]+)&', html) + '?plead=please-dont-download-this-or-our-lawyers-wont-let-us-host-audio'
    elif feed == 'video':
        iframe_url = r1(r'<iframe src=\'([^\']*)\'', html)
        iframe_html = get_html(iframe_url)
        real_url = r1(r'<source src="([^"]*)"', iframe_html)
    else:
        real_url = r1(r'<source src="([^"]*)"', html)

    title = unescape_html(r1(r'<meta property="og:title" content="([^"]*)" />', html) or
        r1(r'<meta property="og:description" content="([^"]*)" />', html) or
        r1(r'<title>([^<\n]*)', html) or url.split("/")[4]).replace('\n', '')

    type, ext, size = url_info(real_url)

    print_info(site_info, title, type, size)
    if not info_only:
        download_urls([real_url], title, ext, size, output_dir, merge = merge)

site_info = "Tumblr.com"
download = tumblr_download
download_playlist = playlist_not_supported('tumblr')
