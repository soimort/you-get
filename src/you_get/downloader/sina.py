#!/usr/bin/env python

__all__ = ['sina_download', 'sina_download_by_vid', 'sina_download_by_vkey']

from ..common import *

def video_info(id):
    xml = get_content('http://v.iask.com/v_play.php?vid=%s' % id, decoded=True)
    urls = re.findall(r'<url>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</url>', xml)
    name = match1(xml, r'<vname>(?:<!\[CDATA\[)?(.+?)(?:\]\]>)?</vname>')
    vstr = match1(xml, r'<vstr>(?:<!\[CDATA\[)?(.+?)(?:\]\]>)?</vstr>')
    return urls, name, vstr

def sina_download_by_vid(vid, title=None, output_dir='.', merge=True, info_only=False):
    """Downloads a Sina video by its unique vid.
    http://video.sina.com.cn/
    """
    
    urls, name, vstr = video_info(vid)
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

def sina_download(url, output_dir='.', merge=True, info_only=False):
    """Downloads Sina videos by URL.
    """
    
    vid = match1(url, r'vid=(\d+)')
    if vid is None:
        video_page = get_content(url)
        vid = hd_vid = match1(video_page, r'hd_vid\s*:\s*\'([^\']+)\'')
        if hd_vid == '0':
            vids = match1(video_page, r'[^\w]vid\s*:\s*\'([^\']+)\'').split('|')
            vid = vids[-1]
    
    if vid:
        sina_download_by_vid(vid, output_dir=output_dir, merge=merge, info_only=info_only)
    else:
        vkey = match1(video_page, r'vkey\s*:\s*"([^"]+)"')
        title = match1(video_page, r'title\s*:\s*"([^"]+)"')
        sina_download_by_vkey(vkey, title=title, output_dir=output_dir, merge=merge, info_only=info_only)

site_info = "Sina.com"
download = sina_download
download_playlist = playlist_not_supported('sina')
