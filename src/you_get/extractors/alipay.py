"""Download publicly accessible Alipay share videos."""

import json
import re
from urllib import error, parse, request

from ..common import (
    download_urls, playlist_not_supported, post_content, print_info,
    urlopen_with_retry,
)

WEBGW = (
    'https://webgw-internet.alipay.com/contentservice/'
    'com.alipay.sofa.function.SOFAFunction/apply/'
    'myjf.yuyan.contentservice.default.ContentWebGWController.list'
)
HEADERS = {
    'x-webgw-appId': '180020010001266490',
    'x-webgw-version': '2.0',
    'Content-Type': 'application/json',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15',
}
CLARITIES = ('1080P_h265_EH', '1080P_h265', '720P_h265', '720P_h264', '540P_h264')


def content_id(text):
    for _ in range(4):
        match = re.search(r'(?:[?&]|\b)contentId=([A-Za-z0-9]+)(?:[^A-Za-z0-9]|$)', text)
        if match:
            return match.group(1)
        decoded = parse.unquote(text)
        if decoded == text:
            break
        text = decoded
    return None


def resolve_content_id(url):
    value = content_id(url)
    if value:
        return value
    with urlopen_with_retry(request.Request(url, headers={'User-Agent': HEADERS['User-Agent']})) as response:
        value = content_id(response.geturl())
        if not value:
            value = content_id(response.read(4 << 20).decode('utf-8', 'ignore'))
    if not value:
        raise ValueError('Alipay: could not find contentId in share URL')
    return value


def fetch_detail(value):
    data = json.loads(post_content(
        WEBGW, headers=HEADERS, post_data_raw=json.dumps({'contentId': value}),
    ))
    if not isinstance(data, dict) or not data.get('success'):
        message = data.get('errorMessage', 'invalid response') if isinstance(data, dict) else 'invalid response'
        raise ValueError('Alipay API error: {}'.format(message))
    result = data.get('resultObj') or {}
    items = result.get('data') or []
    if not items or not isinstance(items[0], dict) or not (items[0].get('video') or {}).get('vid'):
        raise ValueError('Alipay: no video in API response')
    return items[0]


def stream_candidates(original):
    parts = parse.urlsplit(original)
    if parts.scheme not in ('http', 'https') or not parts.netloc:
        raise ValueError('Alipay: invalid video URL')
    prefix, _, clarity = parts.path.rpartition('/')
    if clarity in CLARITIES:
        for candidate in CLARITIES:
            yield parse.urlunsplit(parts._replace(path=prefix + '/' + candidate))
    yield original


def pick_stream(original):
    for url in dict.fromkeys(stream_candidates(original)):
        try:
            with urlopen_with_retry(request.Request(url, headers={'Range': 'bytes=0-0'})) as response:
                if response.status not in (200, 206):
                    continue
                length = response.headers.get('Content-Length', '')
                if response.status == 206:
                    length = response.headers.get('Content-Range', '').partition('/')[2]
                size = int(length)
                if size > 0:
                    return url, size
        except (error.URLError, OSError, ValueError):
            continue
    raise ValueError('Alipay: no available video streams')


def alipay_download(url, output_dir='.', merge=True, info_only=False, **kwargs):
    value = resolve_content_id(url)
    item = fetch_detail(value)
    title = item.get('title') or value
    stream, size = pick_stream(item['video']['vid'])
    print_info('Alipay (支付宝)', title, 'mp4', size)
    if not info_only:
        download_urls([stream], title, 'mp4', size, output_dir=output_dir, merge=merge, **kwargs)


download = alipay_download
download_playlist = playlist_not_supported('alipay')
