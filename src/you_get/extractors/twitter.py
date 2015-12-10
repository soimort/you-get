#!/usr/bin/env python

__all__ = ['twitter_download']

from ..common import *
from .vine import vine_download

def twitter_download(url, output_dir='.', merge=True, info_only=False, **kwargs):
    html = get_html(url)
    screen_name = r1(r'data-screen-name="([^"]*)"', html)
    item_id = r1(r'data-item-id="([^"]*)"', html)
    page_title = "{} [{}]".format(screen_name, item_id)

    try: # extract images
        urls = re.findall(r'property="og:image"\s*content="([^"]+:large)"', html)
        assert urls
        images = []
        for url in urls:
            url = ':'.join(url.split(':')[:-1]) + ':orig'
            filename = parse.unquote(url.split('/')[-1])
            title = '.'.join(filename.split('.')[:-1])
            ext = url.split(':')[-2].split('.')[-1]
            size = int(get_head(url)['Content-Length'])
            images.append({'title': title,
                           'url': url,
                           'ext': ext,
                           'size': size})
        size = sum([image['size'] for image in images])
        print_info(site_info, page_title, images[0]['ext'], size)

        if not info_only:
            for image in images:
                title = image['title']
                ext = image['ext']
                size = image['size']
                url = image['url']
                print_info(site_info, title, ext, size)
                download_urls([url], title, ext, size,
                              output_dir=output_dir)

    except: # extract video
        icards = r1(r'data-src="([^"]*)"', html)
        if icards:
            card = get_html("https://twitter.com" + icards)
            data_player_config = r1(r'data-player-config="([^"]*)"', card)
            if data_player_config is None:
                vine_src = r1(r'<iframe src="([^"]*)"', card)
                vine_download(vine_src, output_dir=output_dir, merge=merge, info_only=info_only)
                return
            data = json.loads(unescape_html(data_player_config))
            source = data['playlist'][0]['source']
        else:
            source = r1(r'<source video-src="([^"]*)"', html)

        mime, ext, size = url_info(source)

        print_info(site_info, page_title, mime, size)
        if not info_only:
            download_urls([source], page_title, ext, size, output_dir, merge=merge)

site_info = "Twitter.com"
download = twitter_download
download_playlist = playlist_not_supported('twitter')
