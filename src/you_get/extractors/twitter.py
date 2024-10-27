#!/usr/bin/env python

__all__ = ['twitter_download']

from ..common import *
from .universal import *

def extract_m3u(source):
    r1 = get_content(source)
    s1 = re.findall(r'(/ext_tw_video/.*)', r1)
    s1 += re.findall(r'(/amplify_video/.*)', r1)
    r2 = get_content('https://video.twimg.com%s' % s1[-1])
    s2 = re.findall(r'(/ext_tw_video/.*)', r2)
    s2 += re.findall(r'(/amplify_video/.*)', r2)
    return ['https://video.twimg.com%s' % i for i in s2]

def twitter_download(url, output_dir='.', merge=True, info_only=False, **kwargs):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0',
        'Accept-Encoding': 'gzip, deflate',
        'Accept': '*/*'
    }

    if re.match(r'https?://pbs\.twimg\.com', url):
        universal_download(url, output_dir, merge=merge, info_only=info_only, **kwargs)
        return

    if re.match(r'https?://mobile', url): # normalize mobile URL
        url = 'https://' + match1(url, r'//mobile\.(.+)')

    if re.match(r'https?://twitter\.com/i/moments/', url): # FIXME: moments
        html = get_html(url, faker=True)
        paths = re.findall(r'data-permalink-path="([^"]+)"', html)
        for path in paths:
            twitter_download('https://twitter.com' + path,
                             output_dir=output_dir,
                             merge=merge,
                             info_only=info_only,
                             **kwargs)
        return

    m = re.match(r'^https?://(mobile\.)?(x|twitter)\.com/([^/]+)/status/(\d+)', url)
    assert m
    screen_name, item_id = m.group(3), m.group(4)
    page_title = "{} [{}]".format(screen_name, item_id)

    # FIXME: this API won't work for protected or nsfw contents
    api_url = 'https://cdn.syndication.twimg.com/tweet-result?id=%s&token=!' % item_id
    content = get_content(api_url)
    info = json.loads(content)

    author = info['user']['name']
    url = 'https://twitter.com/%s/status/%s' % (info['user']['screen_name'], item_id)
    full_text = info['text']

    if 'photos' in info:
        for photo in info['photos']:
            photo_url = photo['url']
            title = item_id + '_' + photo_url.split('.')[-2].split('/')[-1]
            urls = [ photo_url + ':orig' ]
            size = urls_size(urls, headers=headers)
            ext = photo_url.split('.')[-1]

            print_info(site_info, title, ext, size)
            if not info_only:
                download_urls(urls, title, ext, size, output_dir, merge=merge)

    if 'video' in info:
        for mediaDetail in info['mediaDetails']:
            if 'video_info' not in mediaDetail: continue
            variants = mediaDetail['video_info']['variants']
            variants = sorted(variants, key=lambda kv: kv.get('bitrate', 0))
            title = item_id + '_' + variants[-1]['url'].split('/')[-1].split('?')[0].split('.')[0]
            urls = [ variants[-1]['url'] ]
            size = urls_size(urls, headers=headers)
            mime, ext = variants[-1]['content_type'], 'mp4'

            print_info(site_info, title, ext, size)
            if not info_only:
                download_urls(urls, title, ext, size, output_dir, merge=merge, headers=headers)

    # TODO: should we deal with quoted tweets?


site_info = "X.com"
download = twitter_download
download_playlist = playlist_not_supported('twitter')
