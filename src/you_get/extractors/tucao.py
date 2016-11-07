#!/usr/bin/env python

__all__ = ['tucao_download']
from ..common import *
# import re
import random
import time
from xml.dom import minidom
#possible raw list types
#1. <li>type=tudou&vid=199687639</li>
#2. <li>type=tudou&vid=199506910|</li>
#3. <li>type=video&file=http://xiaoshen140731.qiniudn.com/lovestage04.flv|</li>
#4 may ? <li>type=video&file=http://xiaoshen140731.qiniudn.com/lovestage04.flv|xx**type=&vid=?</li>
#5. <li>type=tudou&vid=200003098|07**type=tudou&vid=200000350|08</li>
#6. <li>vid=49454694&type=sina|</li>
#7. <li>type=189&vid=513031813243909|</li>
# re_pattern=re.compile(r"(type=(.+?)&(vid|file)=(.*?))[\|<]")

def tucao_single_download(type_link, title, output_dir=".", merge=True, info_only=False):
    if "file" in type_link:
        url=type_link[type_link.find("file=")+5:]
        vtype, ext, size=url_info(url)
        print_info(site_info, title, vtype, size)
        if not info_only:
            download_urls([url], title, ext, size, output_dir)
    #fix for 189 video source, see raw list types 7
    elif "189" in type_link:
        vid = match1(type_link, r"vid=(\d+)")
        assert vid, "vid not exsits"
        url = "http://api.tucao.tv/api/down/{}".format(vid)
        vtype, ext, size=url_info(url)
        print_info(site_info, title, vtype, size)
        if not info_only:
            download_urls([url], title, ext, size, output_dir)
    else:
        u="http://www.tucao.tv/api/playurl.php?{}&key=tucao{:07x}.cc&r={}".format(type_link,random.getrandbits(28),int(time.time()*1000))
        xml=minidom.parseString(get_content(u))
        urls=[]
        size=0
        for i in xml.getElementsByTagName("url"):
            urls.append(i.firstChild.nodeValue)
            vtype, ext, _size=url_info(i.firstChild.nodeValue)
            size+=_size
        print_info(site_info, title, vtype, size)
        if not info_only:
            download_urls(urls, title, ext, size, output_dir)

def tucao_download(url, output_dir=".", merge=True, info_only=False, **kwargs):
    html=get_content(url)
    title=match1(html,r'<h1 class="show_title">(.*?)<\w')
    #fix for raw list that vid goes before type, see raw list types 6
    raw_list=match1(html,r"<li>\s*(type=.+?|vid=.+?)</li>")
    raw_l=raw_list.split("**")
    if len(raw_l)==1:
        format_link=raw_l[0][:-1] if raw_l[0].endswith("|") else raw_l[0]
        tucao_single_download(format_link,title,output_dir,merge,info_only)
    else:
        for i in raw_l:
            format_link,sub_title=i.split("|")
            tucao_single_download(format_link,title+"-"+sub_title,output_dir,merge,info_only)


site_info = "tucao.tv"
download = tucao_download
download_playlist = playlist_not_supported("tucao")
