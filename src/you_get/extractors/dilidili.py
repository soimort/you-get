#!/usr/bin/env python

__all__ = ['dilidili_download']

from ..common import *
from .ckplayer import ckplayer_download

headers = {
    'DNT': '1',
    'Accept-Encoding': 'gzip, deflate, sdch, br',
    'Accept-Language': 'en-CA,en;q=0.8,en-US;q=0.6,zh-CN;q=0.4,zh;q=0.2',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.75 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Cache-Control': 'max-age=0',
    'Referer': 'http://www.dilidili.com/',
    'Connection': 'keep-alive',
    'Save-Data': 'on',
}

#----------------------------------------------------------------------
def dilidili_parser_data_to_stream_types(typ ,vid ,hd2 ,sign, tmsign, ulk):
    """->list"""
    another_url = 'https://newplayer.jfrft.com/parse.php?xmlurl=null&type={typ}&vid={vid}&hd={hd2}&sign={sign}&tmsign={tmsign}&userlink={ulk}'.format(typ = typ, vid = vid, hd2 = hd2, sign = sign, tmsign = tmsign, ulk = ulk)
    parse_url = 'http://player.005.tv/parse.php?xmlurl=null&type={typ}&vid={vid}&hd={hd2}&sign={sign}&tmsign={tmsign}&userlink={ulk}'.format(typ = typ, vid = vid, hd2 = hd2, sign = sign, tmsign = tmsign, ulk = ulk)
    html = get_content(another_url, headers=headers)
    
    info = re.search(r'(\{[^{]+\})(\{[^{]+\})(\{[^{]+\})(\{[^{]+\})(\{[^{]+\})', html).groups()
    info = [i.strip('{}').split('->') for i in info]
    info = {i[0]: i [1] for i in info}
    
    stream_types = []
    for i in zip(info['deft'].split('|'), info['defa'].split('|')):
        stream_types.append({'id': str(i[1][-1]), 'container': 'mp4', 'video_profile': i[0]})
    return stream_types

#----------------------------------------------------------------------
def dilidili_download(url, output_dir = '.', merge = False, info_only = False, **kwargs):
    global headers
    re_str = r'http://www.dilidili.com/watch\S+'
    if re.match(r'http://www.dilidili.wang', url):
        re_str = r'http://www.dilidili.wang/watch\S+'
        headers['Referer'] = 'http://www.dilidili.wang/'
    elif re.match(r'http://www.dilidili.mobi', url):
        re_str = r'http://www.dilidili.mobi/watch\S+'
        headers['Referer'] = 'http://www.dilidili.mobi/'

    if re.match(re_str, url):
        html = get_content(url)
        title = match1(html, r'<title>(.+)丨(.+)</title>')  #title
        
        # player loaded via internal iframe
        frame_url = re.search(r'<iframe src=\"(.+?)\"', html).group(1)
        logging.debug('dilidili_download: %s' % frame_url)
        
        #https://player.005.tv:60000/?vid=a8760f03fd:a04808d307&v=yun&sign=a68f8110cacd892bc5b094c8e5348432
        html = get_content(frame_url, headers=headers, decoded=False).decode('utf-8')
        
        match = re.search(r'(.+?)var video =(.+?);', html)
        vid = match1(html, r'var vid="(.+)"')
        hd2 = match1(html, r'var hd2="(.+)"')
        typ = match1(html, r'var typ="(.+)"')
        sign = match1(html, r'var sign="(.+)"')
        tmsign = match1(html, r'tmsign=([A-Za-z0-9]+)')
        ulk =  match1(html, r'var ulk="(.+)"')

        # here s the parser...
        stream_types = dilidili_parser_data_to_stream_types(typ, vid, hd2, sign, tmsign, ulk)
        
        #get best
        best_id = max([i['id'] for i in stream_types])
        
        parse_url = 'http://player.005.tv/parse.php?xmlurl=null&type={typ}&vid={vid}&hd={hd2}&sign={sign}&tmsign={tmsign}&userlink={ulk}'.format(typ = typ, vid = vid, hd2 = best_id, sign = sign, tmsign = tmsign, ulk = ulk)
        
        another_url = 'https://newplayer.jfrft.com/parse.php?xmlurl=null&type={typ}&vid={vid}&hd={hd2}&sign={sign}&tmsign={tmsign}&userlink={ulk}'.format(typ = typ, vid = vid, hd2 = hd2, sign = sign, tmsign = tmsign, ulk = ulk)

        ckplayer_download(another_url, output_dir, merge, info_only, is_xml = True, title = title, headers = headers)

        #type_ = ''
        #size = 0

        #type_, ext, size = url_info(url)
        #print_info(site_info, title, type_, size)
        #if not info_only:
            #download_urls([url], title, ext, total_size=None, output_dir=output_dir, merge=merge)

site_info = "dilidili"
download = dilidili_download
download_playlist = playlist_not_supported('dilidili')
