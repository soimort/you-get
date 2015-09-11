#!/usr/bin/env python

__all__ = ['tv66wz_download']
# Attention: It is not possible to name the function as 66wz, so I've put "tv" in front of the names.

from ..common import *
import re

#----------------------------------------------------------------------
def tv66wz_download(url, output_dir = '.', merge = False, info_only = False):
    """str, blahblah->None
    Call the API function"""
    if re.match(r'http://tv.66wz.com/\w+', url):
        
        p = re.compile(r"g_arrVideo\[\d+\] = new videoInfo\((\d+),\d,\'(.+)\',\'")
        
        url_list = []
        
        html = get_content(url)
        
        for m in p.finditer(html):
            url_list.append((m.group(1), m.group(2)))
            #1: id 2: title
        
        for i in url_list:
            tv66wz_download_by_id(i[0], i[1], output_dir='.', merge=False, 
                                 info_only=False)

#----------------------------------------------------------------------
def tv66wz_download_by_id(id, title, output_dir = '.', merge = False, info_only = False):
    """
    str,str, blahblah...-> None
    Attention: title comes from previous function, arguments not exactly the same
    as other extractors"""
    url_httppplay = 'http://60.190.99.171:8080/forcetech/cms/flvhttpplay.jsp?id={id}&type=0&documentID=0&columnID=0'.format(id = id)
    
    html = get_content(url_httppplay)
    
    p = re.compile(r'.+filevalue=(.+)&amp;copyvalue')
    for m in p.finditer(html):
        url = m.group(1)
        break
    
    #print(url)
    
    print('This will take very very long...')
    
    type_, ext, size = url_info(url)
    print_info('66wz', title, 'flv', 0)
    if not info_only:
        download_urls([url], title, 'flv', total_size=None, output_dir=output_dir, merge=merge)

site_info = "66wz"
download = tv66wz_download
download_playlist = playlist_not_supported('66wz')