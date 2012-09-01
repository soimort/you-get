#!/usr/bin/env python

__all__ = ['tudou_download', 'tudou_download_playlist', 'tudou_download_by_id', 'tudou_download_by_iid']

from ..common import *

def tudou_download_by_iid(iid, title, output_dir = '.', merge = True, info_only = False):
    xml = get_html('http://v2.tudou.com/v?it=' + iid + '&st=1,2,3,4,99')
    
    from xml.dom.minidom import parseString
    doc = parseString(xml)
    title = title or doc.firstChild.getAttribute('tt') or doc.firstChild.getAttribute('title')
    urls = [(int(n.getAttribute('brt')), n.firstChild.nodeValue.strip()) for n in doc.getElementsByTagName('f')]
    
    url = max(urls, key = lambda x:x[0])[1]
    assert 'f4v' in url
    
    type, ext, size = url_info(url)
    
    print_info(site_info, title, type, size)
    if not info_only:
        #url_save(url, filepath, bar):
        download_urls([url], title, ext, total_size = None, output_dir = output_dir, merge = merge)

def tudou_download_by_id(id, title, output_dir = '.', merge = True):
    html = get_html('http://www.tudou.com/programs/view/%s/' % id)
    iid = r1(r'iid\s*=\s*(\S+)', html)
    tudou_download_by_iid(iid, title, output_dir = output_dir, merge = merge)

def tudou_download(url, output_dir = '.', merge = True, info_only = False):
    html = get_decoded_html(url)
    
    iid = r1(r'iid\s*[:=]\s*(\d+)', html)
    if not iid:
        tudou_download_playlist(url, output_dir, merge, info_only)
        return
    
    title = r1(r'kw\s*[:=]\s*"([^"]+)"', html)
    assert title
    title = unescape_html(title)
    
    tudou_download_by_iid(iid, title, output_dir = output_dir, merge = merge, info_only = info_only)

def parse_playlist(url):
    aid = r1('http://www.tudou.com/playlist/p/a(\d+)(?:i\d+)?\.html', url)
    html = get_decoded_html(url)
    if not aid:
        aid = r1(r"aid\s*[:=]\s*'(\d+)'", html)
    if re.match(r'http://www.tudou.com/albumcover/', url):
        atitle = r1(r"title\s*:\s*'([^']+)'", html)
    elif re.match(r'http://www.tudou.com/playlist/p/', url):
        atitle = r1(r'atitle\s*=\s*"([^"]+)"', html)
    else:
        raise NotImplementedError(url)
    assert aid
    assert atitle
    import json
    #url = 'http://www.tudou.com/playlist/service/getZyAlbumItems.html?aid='+aid
    url = 'http://www.tudou.com/playlist/service/getAlbumItems.html?aid='+aid
    return [(atitle + '-' + x['title'], str(x['itemId'])) for x in json.loads(get_html(url))['message']]

def tudou_download_playlist(url, output_dir = '.', merge = True, info_only = False):
    videos = parse_playlist(url)
    for i, (title, id) in enumerate(videos):
        print('Processing %s of %s videos...' % (i + 1, len(videos)))
        tudou_download_by_iid(id, title, output_dir = output_dir, merge = merge, info_only = info_only)

site_info = "Tudou.com"
download = tudou_download
download_playlist = tudou_download_playlist
