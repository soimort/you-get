#!/usr/bin/env python
__all__ = ['ixigua_download', 'ixigua_download_playlist']
import base64
import random
import binascii
from ..common import *

headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36'
                  ' (KHTML, like Gecko) Chrome/61.0.3163.100 Mobile Safari/537.36'
}


def get_r():
    return str(random.random())[2:]


def right_shift(val, n):
    return val >> n if val >= 0 else (val + 0x100000000) >> n


def get_s(text):
    """get video info"""
    js_data = json.loads(text)
    id = js_data['data']['video_id']
    p = get_r()
    url = 'http://i.snssdk.com/video/urls/v/1/toutiao/mp4/%s' % id
    n = parse.urlparse(url).path + '?r=%s' % p
    c = binascii.crc32(n.encode('utf-8'))
    s = right_shift(c, 0)
    return url + '?r=%s&s=%s' % (p, s), js_data['data']['title']


def get_moment(url, user_id, base_url, video_list):
    """Recursively obtaining a video list"""
    video_list_data = json.loads(get_content(url, headers=headers))
    if not video_list_data['next']['max_behot_time']:
        return video_list
    [video_list.append(i["display_url"]) for i in video_list_data["data"]]
    max_behot_time = video_list_data['next']['max_behot_time']
    _param = {
        'user_id': user_id,
        'base_url': base_url,
        'video_list': video_list,
        'url': base_url.format(user_id=user_id, max_behot_time=max_behot_time),
    }
    return get_moment(**_param)


def ixigua_download(url, output_dir='.', info_only=False, **kwargs):
    """ Download a single video
        Sample URL: https://www.ixigua.com/a6487187567887254029/#mid=59051127876
    """
    try:
        video_page_id = re.findall('(\d+)', [i for i in url.split('/') if i][3])[0] if 'toutiao.com' in url \
            else re.findall('(\d+)', [i for i in url.split('/') if i][2])[0]

        video_start_info_url = r'https://m.ixigua.com/i{}/info/'.format(video_page_id)
        video_info_url, title = get_s(get_content(video_start_info_url, headers=headers or kwargs.get('headers', {})))
        video_info = json.loads(get_content(video_info_url, headers=headers or kwargs.get('headers', {})))
    except Exception:
        raise NotImplementedError(url)
    try:
        video_url = base64.b64decode(video_info["data"]["video_list"]["video_1"]["main_url"]).decode()
    except Exception:
        raise NotImplementedError(url)
    filetype, ext, size = url_info(video_url, headers=headers or kwargs.get('headers', {}))
    print_info(site_info, title, filetype, size)
    if not info_only:
        _param = {
            'output_dir': output_dir,
            'headers': headers or kwargs.get('headers', {})
        }
        download_urls([video_url], title, ext, size, **_param)


def ixigua_download_playlist(url, output_dir='.', info_only=False, **kwargs):
    """Download all video from the user's video list
        Sample URL: https://www.ixigua.com/c/user/71141690831/
    """
    if 'user' not in url:
        raise NotImplementedError(url)
    user_id = url.split('/')[-2]
    max_behot_time = 0
    if not user_id:
        raise NotImplementedError(url)
    base_url = "https://www.ixigua.com/c/user/article/?user_id={user_id}" \
               "&max_behot_time={max_behot_time}&max_repin_time=0&count=20&page_type=0"
    _param = {
        'user_id': user_id,
        'base_url': base_url,
        'video_list': [],
        'url': base_url.format(user_id=user_id, max_behot_time=max_behot_time),
    }
    for i in get_moment(**_param):
        ixigua_download(i, output_dir, info_only, **kwargs)


site_info = "ixigua.com"
download = ixigua_download
download_playlist = ixigua_download_playlist
