#!/usr/bin/env python

__all__ = ['twitter_download']

from ..common import *
from .vine import vine_download

def extract_m3u(source):
    r1 = get_content(source)
    s1 = re.findall(r'(/ext_tw_video/.*)', r1)
    s1 += re.findall(r'(/amplify_video/.*)', r1)
    r2 = get_content('https://video.twimg.com%s' % s1[-1])
    s2 = re.findall(r'(/ext_tw_video/.*)', r2)
    s2 += re.findall(r'(/amplify_video/.*)', r2)
    return ['https://video.twimg.com%s' % i for i in s2]

def twitter_download(url, output_dir='.', merge=True, info_only=False, **kwargs):
    if re.match(r'https?://mobile', url): # normalize mobile URL
        url = 'https://' + match1(url, r'//mobile\.(.+)')

    if re.match(r'https?://twitter\.com/i/moments/', url): # moments
        html = get_html(url, faker=True)
        paths = re.findall(r'data-permalink-path="([^"]+)"', html)
        for path in paths:
            twitter_download('https://twitter.com' + path,
                             output_dir=output_dir,
                             merge=merge,
                             info_only=info_only,
                             **kwargs)
        return

    html = get_html(url, faker=True)
    screen_name = r1(r'twitter\.com/([^/]+)', url) or r1(r'data-screen-name="([^"]*)"', html) or \
        r1(r'<meta name="twitter:title" content="([^"]*)"', html)
    item_id = r1(r'twitter\.com/[^/]+/status/(\d+)', url) or r1(r'data-item-id="([^"]*)"', html) or \
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
        #i_url = 'https://twitter.com/i/videos/' + item_id
        #i_content = get_content(i_url)
        #js_url = r1(r'src="([^"]+)"', i_content)
        #js_content = get_content(js_url)
        #authorization = r1(r'"(Bearer [^"]+)"', js_content)
        authorization = 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA'

        ga_url = 'https://api.twitter.com/1.1/guest/activate.json'
        ga_content = post_content(ga_url, headers={'authorization': authorization})
        guest_token = json.loads(ga_content)['guest_token']

        api_url = 'https://api.twitter.com/2/timeline/conversation/%s.json?tweet_mode=extended' % item_id
        api_content = get_content(api_url, headers={'authorization': authorization, 'x-guest-token': guest_token})

        info = json.loads(api_content)
        variants = info['globalObjects']['tweets'][item_id]['extended_entities']['media'][0]['video_info']['variants']
        variants = sorted(variants, key=lambda kv: kv.get('bitrate', 0))
        urls = [ variants[-1]['url'] ]
        size = urls_size(urls)
        mime, ext = variants[-1]['content_type'], 'mp4'

        print_info(site_info, page_title, mime, size)
        if not info_only:
            download_urls(urls, page_title, ext, size, output_dir, merge=merge)

site_info = "Twitter.com"
download = twitter_download
download_playlist = playlist_not_supported('twitter')
