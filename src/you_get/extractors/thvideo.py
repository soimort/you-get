#!/usr/bin/env python

__all__ = ['thvideo_download']

from ..common import *
from xml.dom.minidom import parseString

#----------------------------------------------------------------------
def thvideo_cid_to_url(cid, p):
    """int,int->list
    From Biligrab."""
    interface_url = 'http://thvideo.tv/api/playurl.php?cid={cid}-{p}'.format(cid = cid, p = p)
    data = get_content(interface_url)
    rawurl = []
    dom = parseString(data)
    
    for node in dom.getElementsByTagName('durl'):
        url = node.getElementsByTagName('url')[0]
        rawurl.append(url.childNodes[0].data)
    return rawurl

#----------------------------------------------------------------------
def th_video_get_title(url, p):
    """"""
    if re.match(r'http://thvideo.tv/v/\w+', url):
        html = get_content(url)
        title = match1(html, r'<meta property="og:title" content="([^"]*)"').strip()
        
        video_list = match1(html, r'<li>cid=(.+)</li>').split('**')
        
        if int(p) > 0:  #not the 1st P or multi part
            title = title + ' - ' + [i.split('=')[-1:][0].split('|')[1] for i in video_list][p]
            
    return title

#----------------------------------------------------------------------
def thvideo_download(url, output_dir = '.', merge = False, info_only = False, **kwargs):
    if re.match(r'http://thvideo.tv/v/\w+', url):
        if 'p' in kwargs and kwargs['p']:
            p = kwargs['p']
        else:
            p = int(match1(url, r'http://thvideo.tv/v/th\d+#(\d+)'))
            p -= 1
            
            if not p or p < 0:
                p = 0
        
        if 'title' in kwargs and kwargs['title']:
            title = kwargs['title']
        else:
            title = th_video_get_title(url, p)
        
        cid = match1(url, r'http://thvideo.tv/v/th(\d+)')
        
        type_ = ''
        size = 0
        urls = thvideo_cid_to_url(cid, p)
        
        for url in urls:
            _, type_, temp = url_info(url)
            size += temp
        
        print_info(site_info, title, type_, size)
        if not info_only:
            download_urls(urls, title, type_, total_size=None, output_dir=output_dir, merge=merge)

#----------------------------------------------------------------------
def thvideo_download_playlist(url, output_dir = '.', merge = False, info_only = False, **kwargs):
    """"""
    if re.match(r'http://thvideo.tv/v/\w+', url):
        html = get_content(url)
        video_list = match1(html, r'<li>cid=(.+)</li>').split('**')
        
        title_base = th_video_get_title(url, 0)
        for p, v in video_list:
            part_title = [i.split('=')[-1:][0].split('|')[1] for i in video_list][p]
            title = title_base + part_title
            thvideo_download(url, output_dir, merge, 
                            info_only, p = p, title = title)

site_info = "THVideo"
download = thvideo_download
download_playlist = thvideo_download_playlist
