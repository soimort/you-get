#!/usr/bin/env python

__all__ = ['twitter_download']

from ..common import *
from .universal import *
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
    if re.match(r'https?://pbs\.twimg\.com', url):
        universal_download(url, output_dir, merge=merge, info_only=info_only, **kwargs)
        return

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

    html = get_html(url, faker=True) # now it seems faker must be enabled
    screen_name = r1(r'twitter\.com/([^/]+)', url) or r1(r'data-screen-name="([^"]*)"', html) or \
        r1(r'<meta name="twitter:title" content="([^"]*)"', html)
    item_id = r1(r'twitter\.com/[^/]+/status/(\d+)', url) or r1(r'data-item-id="([^"]*)"', html) or \
        r1(r'<meta name="twitter:site:id" content="([^"]*)"', html)
    page_title = "{} [{}]".format(screen_name, item_id)

    authorization = 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA'

    ga_url = 'https://api.twitter.com/1.1/guest/activate.json'
    ga_content = post_content(ga_url, headers={'authorization': authorization})
    guest_token = json.loads(ga_content)['guest_token']

    api_url = 'https://api.twitter.com/2/timeline/conversation/%s.json?tweet_mode=extended' % item_id
    api_content = get_content(api_url, headers={'authorization': authorization, 'x-guest-token': guest_token})

    info = json.loads(api_content)
    if 'extended_entities' in info['globalObjects']['tweets'][item_id]:
        # if the tweet contains media, download them
        media = info['globalObjects']['tweets'][item_id]['extended_entities']['media']

    elif info['globalObjects']['tweets'][item_id].get('is_quote_status') == True:
        # if the tweet does not contain media, but it quotes a tweet
        # and the quoted tweet contains media, download them
        item_id = info['globalObjects']['tweets'][item_id]['quoted_status_id_str']

        api_url = 'https://api.twitter.com/2/timeline/conversation/%s.json?tweet_mode=extended' % item_id
        api_content = get_content(api_url, headers={'authorization': authorization, 'x-guest-token': guest_token})

        info = json.loads(api_content)

        if 'extended_entities' in info['globalObjects']['tweets'][item_id]:
            media = info['globalObjects']['tweets'][item_id]['extended_entities']['media']
        else:
            # quoted tweet has no media
            return

    else:
        # no media, no quoted tweet
        return

    for medium in media:
        if 'video_info' in medium:
            # FIXME: we're assuming one tweet only contains one video here
            variants = medium['video_info']['variants']
            variants = sorted(variants, key=lambda kv: kv.get('bitrate', 0))
            urls = [ variants[-1]['url'] ]
            size = urls_size(urls)
            mime, ext = variants[-1]['content_type'], 'mp4'

            print_info(site_info, page_title, mime, size)
            if not info_only:
                download_urls(urls, page_title, ext, size, output_dir, merge=merge)

        else:
            title = item_id + '_' + medium['media_url_https'].split('.')[-2].split('/')[-1]
            urls = [ medium['media_url_https'] + ':orig' ]
            size = urls_size(urls)
            ext = medium['media_url_https'].split('.')[-1]

            print_info(site_info, title, ext, size)
            if not info_only:
                download_urls(urls, title, ext, size, output_dir, merge=merge)


site_info = "Twitter.com"
download = twitter_download
download_playlist = playlist_not_supported('twitter')
