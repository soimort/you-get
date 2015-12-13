#!/usr/bin/env python

__all__ = ['miomio_download']

from ..common import *

from .tudou import tudou_download_by_id
from .youku import youku_download_by_vid
from xml.dom.minidom import parseString

def miomio_download(url, output_dir = '.', merge = True, info_only = False, **kwargs):
    html = get_html(url)

    fake_headers = {
        'DNT': '1',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'en-CA,en;q=0.8,en-US;q=0.6,zh-CN;q=0.4,zh;q=0.2',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.58 Safari/537.36',
        'Accept': '*/*',
        'X-Requested-With': 'ShockwaveFlash/19.0.0.245',
        'Connection': 'keep-alive',
        'Referer': 'http://www.miomio.tv/',
    }

    title = r1(r'<meta name="description" content="([^"]*)"', html)
    flashvars = r1(r'flashvars="(type=[^"]*)"', html)

    t = r1(r'type=(\w+)', flashvars)
    id = r1(r'vid=([^"]+)', flashvars)
    if t == 'youku':
        youku_download_by_vid(id, title=title, output_dir=output_dir, merge=merge, info_only=info_only)
    elif t == 'tudou':
        tudou_download_by_id(id, title, output_dir=output_dir, merge=merge, info_only=info_only)
    elif t == 'sina' or t == 'video':
        fake_headers['Referer'] = url
        url = "http://www.miomio.tv/mioplayer/mioplayerconfigfiles/sina.php?vid=" + id
        xml_data = get_content(url, headers=fake_headers, decoded=True)
        url_list = sina_xml_to_url_list(xml_data)

        size_full = 0
        for url in url_list:
            type_, ext, size = url_info(url, headers = fake_headers)
            size_full += size
        
        print_info(site_info, title, type_, size_full)
        if not info_only:
            download_urls([url], title, ext, total_size=None, output_dir=output_dir, merge=merge, headers = fake_headers)        
    else:
        raise NotImplementedError(flashvars)

#----------------------------------------------------------------------
def sina_xml_to_url_list(xml_data):
    """str->list
    Convert XML to URL List.
    From Biligrab.
    """
    rawurl = []
    dom = parseString(xml_data)
    for node in dom.getElementsByTagName('durl'):
        url = node.getElementsByTagName('url')[0]
        rawurl.append(url.childNodes[0].data)
    return rawurl

site_info = "MioMio.tv"
download = miomio_download
download_playlist = playlist_not_supported('miomio')
