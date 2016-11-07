#!/usr/bin/env python

__all__ = ['sina_download', 'sina_download_by_vid', 'sina_download_by_vkey']

from ..common import *

from hashlib import md5
from random import randint
from time import time

def get_k(vid, rand):
    t = str(int('{0:b}'.format(int(time()))[:-6], 2))
    return md5((vid + 'Z6prk18aWxP278cVAH' + t + rand).encode('utf-8')).hexdigest()[:16] + t

def video_info_xml(vid):
    rand = "0.{0}{1}".format(randint(10000, 10000000), randint(10000, 10000000))
    url = 'http://ask.ivideo.sina.com.cn/v_play.php?vid={0}&ran={1}&p=i&k={2}'.format(vid, rand, get_k(vid, rand))
    xml = get_content(url, headers=fake_headers, decoded=True)
    return xml

def video_info(xml):
    urls = re.findall(r'<url>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</url>', xml)
    name = match1(xml, r'<vname>(?:<!\[CDATA\[)?(.+?)(?:\]\]>)?</vname>')
    vstr = match1(xml, r'<vstr>(?:<!\[CDATA\[)?(.+?)(?:\]\]>)?</vstr>')
    return urls, name, vstr

def sina_download_by_vid(vid, title=None, output_dir='.', merge=True, info_only=False):
    """Downloads a Sina video by its unique vid.
    http://video.sina.com.cn/
    """

    xml = video_info_xml(vid)
    sina_download_by_xml(xml, title, output_dir, merge, info_only)


def sina_download_by_xml(xml, title, output_dir, merge, info_only):
    urls, name, vstr = video_info(xml)
    title = title or name
    assert title
    size = 0
    for url in urls:
        _, _, temp = url_info(url)
        size += temp

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

def sina_download(url, output_dir='.', merge=True, info_only=False, **kwargs):
    """Downloads Sina videos by URL.
    """

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
        title = match1(video_page, r'title\s*:\s*\'([^\']+)\'')
        sina_download_by_vid(vid, title=title, output_dir=output_dir, merge=merge, info_only=info_only)
    else:
        vkey = match1(video_page, r'vkey\s*:\s*"([^"]+)"')
        title = match1(video_page, r'title\s*:\s*"([^"]+)"')
        sina_download_by_vkey(vkey, title=title, output_dir=output_dir, merge=merge, info_only=info_only)

site_info = "Sina.com"
download = sina_download
download_playlist = playlist_not_supported('sina')
