#!/usr/bin/env python

__all__ = ['suntv_download']

from ..common import *
import urllib
import re

def suntv_download(url, output_dir = '.', merge = True, info_only = False, **kwargs):
    if re.match(r'http://www.isuntv.com/\w+', url):
        API_URL = "http://www.isuntv.com/ajaxpro/SunTv.pro_vod_playcatemp4,App_Web_playcatemp4.ascx.9f08f04f.ashx"
        
        itemid = match1(url, r'http://www.isuntv.com/pro/ct(\d+).html')
        values = {"itemid" : itemid, "vodid": ""}
        
        data = str(values).replace("'", '"')
        data = data.encode('utf-8')
        req = urllib.request.Request(API_URL, data)
        req.add_header('AjaxPro-Method', 'ToPlay')  #important!
        resp = urllib.request.urlopen(req)
        respData = resp.read()
        respData = respData.decode('ascii').strip('"')  #Ahhhhhhh!
    
        video_url = 'http://www.isuntv.com' + str(respData)
        
        html = get_content(url, decoded=False)
        html = html.decode('gbk')
        title = match1(html, '<title>([^<]+)').strip()  #get rid of \r\n s
        
        type_ = ''
        size = 0
        type, ext, size = url_info(video_url)
        
        print_info(site_info, title, type, size)
        if not info_only:
            download_urls([url], title, 'mp4', size, output_dir, merge=merge)

site_info = "SunTV"
download = suntv_download
download_playlist = playlist_not_supported('suntv')
