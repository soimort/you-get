#!/usr/bin/env python

__all__ = ['nanagogo_download']

from ..common import *
from .universal import *

def nanagogo_download(url, output_dir='.', merge=True, info_only=False, **kwargs):
    if re.match(r'https?://stat.7gogo.jp', url):
        universal_download(url, output_dir, merge=merge, info_only=info_only)
        return

    talk_id = r1(r'7gogo.jp/([^/]+)/', url)
    post_id = r1(r'7gogo.jp/[^/]+/(\d+)', url)
    title = '%s_%s' % (talk_id, post_id)
    api_url = 'https://api.7gogo.jp/web/v2/talks/%s/posts/%s' % (talk_id, post_id)
    info = json.loads(get_content(api_url))

    items = []
    if info['data']['posts']['post'] is None:
        return
    if info['data']['posts']['post']['body'] is None:
        return
    for i in info['data']['posts']['post']['body']:
        if 'image' in i:
            image_url = i['image']
            if image_url[:2] == '//': continue # skip stamp images
            _, ext, size = url_info(image_url)
            items.append({'title': title,
                          'url':   image_url,
                          'ext':   ext,
                          'size':  size})
        elif 'movieUrlHq' in i:
            movie_url = i['movieUrlHq']
            _, ext, size = url_info(movie_url)
            items.append({'title': title,
                          'url':   movie_url,
                          'ext':   ext,
                          'size':  size})

    size = sum([i['size'] for i in items])
    if size == 0: return # do not fail the whole process
    print_info(site_info, title, ext, size)
    if not info_only:
        for i in items:
            print_info(site_info, i['title'], i['ext'], i['size'])
            download_urls([i['url']], i['title'], i['ext'], i['size'],
                          output_dir=output_dir,
                          merge=merge)

site_info = "7gogo.jp"
download = nanagogo_download
download_playlist = playlist_not_supported('nanagogo')
