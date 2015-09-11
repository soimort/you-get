#!/usr/bin/env python

__all__ = ['tv66wz_download']
# Attention: It is not possible to name the function as 66wz, so I've put "tv" in front of the names.

from ..common import *
import re
import urllib.parse as urlparse
import http.client as httplib

#----------------------------------------------------------------------
def resolve_http_redirect(url, depth=0):
    """http://www.zacwitte.com/resolving-http-redirects-in-python
    """
    if depth > 10:
        raise Exception("Redirected "+depth+" times, giving up.")
    o = urlparse.urlparse(url,allow_fragments=True)
    conn = httplib.HTTPConnection(o.netloc)
    path = o.path
    if o.query:
        path +='?'+o.query
    conn.request("HEAD", path)
    res = conn.getresponse()
    headers = dict(res.getheaders())
    if 'Location' in headers and headers['Location'] != url:
        return resolve_http_redirect(headers['Location'], depth+1)
    else:
        return url


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
        url_temp = m.group(1)
        break
    
    url = resolve_http_redirect(url_temp)
    
    type_, ext, size = url_info(url)
    print_info('66wz', title, 'flv', size)
    if not info_only:
        download_urls([url], title, ext, total_size=None, output_dir=output_dir, merge=merge)

site_info = "66wz"
download = tv66wz_download
download_playlist = playlist_not_supported('66wz')