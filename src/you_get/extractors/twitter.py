#!/usr/bin/env python

__all__ = ['twitter_download']

from ..common import *
from .vine import vine_download

def extract_m3u(source):
    r1 = get_content(source)
    s1 = re.findall(r'(/ext_tw_video/.*)', r1)
    r2 = get_content('https://video.twimg.com%s' % s1[-1])
    s2 = re.findall(r'(/ext_tw_video/.*)', r2)
    return ['https://video.twimg.com%s' % i for i in s2]

def twitter_download(url, output_dir='.', merge=True, info_only=False, **kwargs):
    html = get_html(url)
    screen_name = r1(r'data-screen-name="([^"]*)"', html) or \
        r1(r'<meta name="twitter:title" content="([^"]*)"', html)
    item_id = r1(r'data-item-id="([^"]*)"', html) or \
        r1(r'<meta name="twitter:site:id" content="([^"]*)"', html)
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
        # always use i/cards or videos url
        if not re.match(r'https?://twitter.com/i/', url):
            url = r1(r'<meta\s*property="og:video:url"\s*content="([^"]+)"', html)
            if not url:
                url = 'https://twitter.com/i/videos/%s' % item_id
            html = get_content(url)

        data_config = r1(r'data-config="([^"]*)"', html) or \
            r1(r'data-player-config="([^"]*)"', html)
        i = json.loads(unescape_html(data_config))
        if 'video_url' in i:
            source = i['video_url']
            if not item_id: page_title = i['tweet_id']
        elif 'playlist' in i:
            source = i['playlist'][0]['source']
            if not item_id: page_title = i['playlist'][0]['contentId']
        elif 'vmap_url' in i:
            vmap_url = i['vmap_url']
            vmap = get_content(vmap_url)
            source = r1(r'<MediaFile>\s*<!\[CDATA\[(.*)\]\]>', vmap)
            if not item_id: page_title = i['tweet_id']
        elif 'scribe_playlist_url' in i:
            scribe_playlist_url = i['scribe_playlist_url']
            return vine_download(scribe_playlist_url, output_dir, merge=merge, info_only=info_only)

        try:
            urls = extract_m3u(source)
        except:
            urls = [source]
        size = urls_size(urls)
        mime, ext = 'video/mp4', 'mp4'

        print_info(site_info, page_title, mime, size)
        if not info_only:
            download_urls(urls, page_title, ext, size, output_dir, merge=merge)

site_info = "Twitter.com"
download = twitter_download
download_playlist = playlist_not_supported('twitter')
