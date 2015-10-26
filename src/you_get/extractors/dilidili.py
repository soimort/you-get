#!/usr/bin/env python

__all__ = ['dilidili_download']

from ..common import *

#----------------------------------------------------------------------
def dilidili_parser_data_to_stream_types(typ ,vid ,hd2 ,sign):
    """->list"""
    parse_url = 'http://player.005.tv/parse.php?xmlurl=null&type={typ}&vid={vid}&hd={hd2}&sign={sign}'.format(typ = typ, vid = vid, hd2 = hd2, sign = sign)
    html = get_html(parse_url)
    
    info = re.search(r'(\{[^{]+\})(\{[^{]+\})(\{[^{]+\})(\{[^{]+\})(\{[^{]+\})', html).groups()
    info = [i.strip('{}').split('->') for i in info]
    info = {i[0]: i [1] for i in info}
    
    stream_types = []
    for i in zip(info['deft'].split('|'), info['defa'].split('|')):
        stream_types.append({'id': str(i[1][-1]), 'container': 'mp4', 'video_profile': i[0]})
    return stream_types

#----------------------------------------------------------------------
def dilidili_parser_data_to_download_url(typ ,vid ,hd2 ,sign):
    """->str"""
    parse_url = 'http://player.005.tv/parse.php?xmlurl=null&type={typ}&vid={vid}&hd={hd2}&sign={sign}'.format(typ = typ, vid = vid, hd2 = hd2, sign = sign)
    html = get_html(parse_url)
    
    return match1(html, r'<file><!\[CDATA\[(.+)\]\]></file>')

#----------------------------------------------------------------------
def dilidili_download(url, output_dir = '.', merge = False, info_only = False, **kwargs):
    if re.match(r'http://www.dilidili.com/watch/\w+', url):
        html = get_html(url)
        title = match1(html, r'<title>(.+)丨(.+)</title>')  #title
        
        # player loaded via internal iframe
        frame_url = re.search(r'<iframe (.+)src="(.+)\" f(.+)</iframe>', html).group(2)
        #https://player.005.tv:60000/?vid=a8760f03fd:a04808d307&v=yun&sign=a68f8110cacd892bc5b094c8e5348432
        html = get_html(frame_url)
        
        match = re.search(r'(.+?)var video =(.+?);', html)
        vid = match1(html, r'var vid="(.+)"')
        hd2 = match1(html, r'var hd2="(.+)"')
        typ = match1(html, r'var typ="(.+)"')
        sign = match1(html, r'var sign="(.+)"')
        
        # here s the parser...
        stream_types = dilidili_parser_data_to_stream_types(typ, vid, hd2, sign)
        
        #get best
        best_id = max([i['id'] for i in stream_types])
        
        url = dilidili_parser_data_to_download_url(typ, vid, best_id, sign)

        type_ = ''
        size = 0

        type_, ext, size = url_info(url)
        print_info(site_info, title, type_, size)
        if not info_only:
            download_urls([url], title, ext, total_size=None, output_dir=output_dir, merge=merge)

site_info = "dilidili"
download = dilidili_download
download_playlist = playlist_not_supported('dilidili')
