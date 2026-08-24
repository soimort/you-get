#!/usr/bin/env python

__all__ = ['twitter_download']

import os
from urllib.parse import parse_qs, urlparse

from ..common import *
from .universal import *

XQUIK_TWEET_URL = 'https://xquik.com/api/v1/x/tweets/{}'


def _tweet_id(url):
    match = re.match(
        r'^https?://(?:(?:mobile|www)\.)?(?:x|twitter)\.com/[^/]+/status/(\d+)',
        url
    )
    assert match
    return match.group(1)


def _media_extension(url, default):
    parsed = urlparse(url)
    query_format = parse_qs(parsed.query).get('format')
    if query_format:
        return query_format[0]
    extension = os.path.splitext(parsed.path)[1].lstrip('.')
    return extension or default


def _xquik_info(item_id, api_key, fetch=get_content):
    content = fetch(
        XQUIK_TWEET_URL.format(item_id),
        headers={'x-api-key': api_key}
    )
    media_items = json.loads(content)['tweet'].get('media', [])
    info = {'photos': [], 'mediaDetails': []}

    for media in media_items:
        media_type = media.get('type')
        if media_type == 'photo':
            media_url = media.get('mediaUrl')
            if media_url:
                info['photos'].append({
                    'url': media_url,
                    'download_url': media_url
                })
        elif media_type in ('video', 'animated_gif'):
            variants = [
                {
                    'bitrate': variant.get('bitrate', 0),
                    'content_type': variant['contentType'],
                    'url': variant['url']
                }
                for variant in media.get('videoVariants', [])
                if variant.get('contentType') == 'video/mp4'
                and variant.get('url')
            ]
            if variants:
                info['mediaDetails'].append({
                    'video_info': {'variants': variants}
                })

    return info


def _has_media(info):
    return bool(info.get('photos') or info.get('mediaDetails'))


def _tweet_info(item_id, api_key, fetch=get_content):
    api_url = 'https://cdn.syndication.twimg.com/tweet-result?id=%s&token=!' % item_id
    info = json.loads(fetch(api_url))
    if _has_media(info) or not api_key:
        return info
    xquik_info = _xquik_info(item_id, api_key, fetch=fetch)
    return xquik_info if _has_media(xquik_info) else info


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

    if re.match(r'https?://mobile', url):  # normalize mobile URL
        url = 'https://' + match1(url, r'//mobile\.(.+)')

    if re.match(r'https?://twitter\.com/i/moments/', url):  # FIXME: moments
        html = get_html(url, faker=True)
        paths = re.findall(r'data-permalink-path="([^"]+)"', html)
        for path in paths:
            twitter_download('https://twitter.com' + path,
                             output_dir=output_dir,
                             merge=merge,
                             info_only=info_only,
                             **kwargs)
        return

    item_id = _tweet_id(url)

    xquik_api_key = os.environ.get('XQUIK_API_KEY')
    info = _tweet_info(item_id, xquik_api_key)

    if 'photos' in info:
        for photo in info['photos']:
            photo_url = photo['url']
            media_name = os.path.splitext(os.path.basename(urlparse(photo_url).path))[0]
            title = item_id + '_' + media_name
            urls = [photo.get('download_url', photo_url + ':orig')]
            size = urls_size(urls, headers=headers)
            ext = _media_extension(photo_url, 'jpg')

            print_info(site_info, title, ext, size)
            if not info_only:
                download_urls(urls, title, ext, size, output_dir, merge=merge)

    for mediaDetail in info.get('mediaDetails', []):
        if 'video_info' in mediaDetail:
            variants = mediaDetail['video_info']['variants']
            variants = sorted(variants, key=lambda kv: kv.get('bitrate', 0))
            media_url = variants[-1]['url']
            media_name = os.path.splitext(os.path.basename(urlparse(media_url).path))[0]
            title = item_id + '_' + media_name
            urls = [media_url]
            size = urls_size(urls, headers=headers)
            ext = 'mp4'

            print_info(site_info, title, ext, size)
            if not info_only:
                download_urls(urls, title, ext, size, output_dir, merge=merge, headers=headers)

    # TODO: should we deal with quoted tweets?


site_info = "X.com"
download = twitter_download
download_playlist = playlist_not_supported('twitter')
