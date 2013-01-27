#!/usr/bin/env python

__all__ = ['iqiyi_download']

from ..common import *

def iqiyi_download(url, output_dir = '.', merge = True, info_only = False):
    html = get_html(url)
    #title = r1(r'title\s*:\s*"([^"]+)"', html)
    #title = unescape_html(title).decode('utf-8')
    #videoId = r1(r'videoId\s*:\s*"([^"]+)"', html)
    #pid = r1(r'pid\s*:\s*"([^"]+)"', html)
    #ptype = r1(r'ptype\s*:\s*"([^"]+)"', html)
    #info_url = 'http://cache.video.qiyi.com/v/%s/%s/%s/' % (videoId, pid, ptype)
    videoId = r1(r'''["']videoId["'][:=]["']([^"']+)["']''', html)
    assert videoId
    
    info_url = 'http://cache.video.qiyi.com/v/%s' % videoId
    info_xml = get_html(info_url)
    
    from xml.dom.minidom import parseString
    doc = parseString(info_xml)
    title = doc.getElementsByTagName('title')[0].firstChild.nodeValue
    size = int(doc.getElementsByTagName('totalBytes')[0].firstChild.nodeValue)
    urls = [n.firstChild.nodeValue for n in doc.getElementsByTagName('file')]
    assert urls[0].endswith('.f4v'), urls[0]
    
    for i in range(len(urls)):
        temp_url = "http://data.video.qiyi.com/%s" % urls[i].split("/")[-1].split(".")[0] + ".ts"
        try:
            response = request.urlopen(temp_url)
        except request.HTTPError as e:
            key = r1(r'key=(.*)', e.geturl())
        assert key
        urls[i] += "?key=%s" % key
    
    print_info(site_info, title, 'flv', size)
    if not info_only:
        download_urls(urls, title, 'flv', size, output_dir = output_dir, merge = merge)

site_info = "iQIYI.com"
download = iqiyi_download
download_playlist = playlist_not_supported('iqiyi')
