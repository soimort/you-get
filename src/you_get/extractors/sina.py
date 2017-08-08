#!/usr/bin/env python

__all__ = ['sina_download', 'sina_download_by_vid', 'sina_download_by_vkey']

from ..common import *
from ..util.log import *

from hashlib import md5
from random import randint
from time import time
from xml.dom.minidom import parseString
import urllib.parse

def api_req(vid):
    rand = "0.{0}{1}".format(randint(10000, 10000000), randint(10000, 10000000))
    t = str(int('{0:b}'.format(int(time()))[:-6], 2))
    k = md5((vid + 'Z6prk18aWxP278cVAH' + t + rand).encode('utf-8')).hexdigest()[:16] + t
    url = 'http://ask.ivideo.sina.com.cn/v_play.php?vid={0}&ran={1}&p=i&k={2}'.format(vid, rand, k)
    xml = get_content(url, headers=fake_headers)
    return xml

def video_info(xml):
    video = parseString(xml).getElementsByTagName('video')[0]
    result = video.getElementsByTagName('result')[0]
    if result.firstChild.nodeValue == 'error':
        message = video.getElementsByTagName('message')[0]
        return None, message.firstChild.nodeValue, None
    vname = video.getElementsByTagName('vname')[0].firstChild.nodeValue
    durls = video.getElementsByTagName('durl')

    urls = []
    size = 0
    for durl in durls:
        url = durl.getElementsByTagName('url')[0].firstChild.nodeValue
        seg_size = durl.getElementsByTagName('filesize')[0].firstChild.nodeValue
        urls.append(url)
        size += int(seg_size)

    return urls, vname, size

def sina_download_by_vid(vid, title=None, output_dir='.', merge=True, info_only=False):
    """Downloads a Sina video by its unique vid.
    http://video.sina.com.cn/
    """
    xml = api_req(vid)
    urls, name, size = video_info(xml)
    if urls is None:
        log.wtf(name)
    title = name
    print_info(site_info, title, 'flv', size)
    if not info_only:
        download_urls(urls, title, 'flv', size, output_dir = output_dir, merge = merge)

def sina_download_by_vkey(vkey, title=None, output_dir='.', merge=True, info_only=False):
    """Downloads a Sina video by its unique vkey.
    http://video.sina.com/
    """

    url = 'http://video.sina.com/v/flvideo/%s_0.flv' % vkey
    type, ext, size = url_info(url)

    print_info(site_info, title, 'flv', size)
    if not info_only:
        download_urls([url], title, 'flv', size, output_dir = output_dir, merge = merge)

def sina_zxt(url, output_dir='.', merge=True, info_only=False, **kwargs):
    ep = 'http://s.video.sina.com.cn/video/play?video_id='
    frag = urllib.parse.urlparse(url).fragment
    if not frag:
        log.wtf('No video specified with fragment')
    meta = json.loads(get_content(ep + frag))
    if meta['code'] != 1:
# Yes they use 1 for success.
        log.wtf(meta['message'])
    title = meta['data']['title']
    videos = sorted(meta['data']['videos'], key = lambda i: int(i['size']))

    if len(videos) == 0:
        log.wtf('No video file returned by API server')

    vid = videos[-1]['file_id']
    container = videos[-1]['type']
    size = int(videos[-1]['size'])

    if container == 'hlv':
        container = 'flv'

    urls, _, _ = video_info(api_req(vid))
    print_info(site_info, title, container, size)
    if not info_only:
        download_urls(urls, title, container, size, output_dir=output_dir, merge=merge, **kwargs)
    return

def sina_download(url, output_dir='.', merge=True, info_only=False, **kwargs):
    """Downloads Sina videos by URL.
    """
    if 'news.sina.com.cn/zxt' in url:
        sina_zxt(url, output_dir=output_dir, merge=merge, info_only=info_only, **kwargs)
        return

    vid = match1(url, r'vid=(\d+)')
    if vid is None:
        video_page = get_content(url)
        vid = hd_vid = match1(video_page, r'hd_vid\s*:\s*\'([^\']+)\'')
        if hd_vid == '0':
            vids = match1(video_page, r'[^\w]vid\s*:\s*\'([^\']+)\'').split('|')
            vid = vids[-1]

    if vid is None:
        vid = match1(video_page, r'vid:"?(\d+)"?')
    if vid:
        #title = match1(video_page, r'title\s*:\s*\'([^\']+)\'')
        sina_download_by_vid(vid, output_dir=output_dir, merge=merge, info_only=info_only)
    else:
        vkey = match1(video_page, r'vkey\s*:\s*"([^"]+)"')
        if vkey is None:
            vid = match1(url, r'#(\d+)')
            sina_download_by_vid(vid, output_dir=output_dir, merge=merge, info_only=info_only)
            return
        title = match1(video_page, r'title\s*:\s*"([^"]+)"')
        sina_download_by_vkey(vkey, title=title, output_dir=output_dir, merge=merge, info_only=info_only)

site_info = "Sina.com"
download = sina_download
download_playlist = playlist_not_supported('sina')
