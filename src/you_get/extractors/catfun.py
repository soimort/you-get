#!/usr/bin/env python

__all__ = ['catfun_download']
from .tudou import tudou_download_by_id
from .sina import sina_download_by_vid

from ..common import *
from xml.dom.minidom import *

def parse_item(item):
    if item["type"] == "youku":
        page = get_content("http://www.catfun.tv/index.php?m=catfun&c=catfun_video&a=get_youku_video_info&youku_id=" + item["vid"])
        dom = parseString(page)
        ext = dom.getElementsByTagName("format")[0].firstChild.nodeValue;
        size = 0
        urls = []
        for i in dom.getElementsByTagName("durl"):
            urls.append(i.getElementsByTagName("url")[0].firstChild.nodeValue)
            size += int(i.getElementsByTagName("size")[0].firstChild.nodeValue);
        return urls, ext, size

    elif item["type"] == "qq":
        page = get_content("http://www.catfun.tv/index.php?m=catfun&c=catfun_video&a=get_qq_video_info&qq_id=" + item["vid"])
        dom = parseString(page)
        size = 0
        urls = []
        for i in dom.getElementsByTagName("durl"):
            url = i.getElementsByTagName("url")[0].firstChild.nodeValue
            urls.append(url)
            vtype, ext, _size = url_info(url)
            size += _size
        return urls, ext, size

    elif item["type"] == "sina":
        page = get_content("http://www.catfun.tv/index.php?m=catfun&c=catfun_video&a=get_sina_video_info&sina_id=" + item["vid"])
        try:
            dom = parseString(page)
        except:
            #refresh page encountered
            page = get_content(match1(page, r'url=(.+?)"'))
            dom = parseString(page)
        size = 0
        urls = []
        for i in dom.getElementsByTagName("durl"):
            url = i.getElementsByTagName("url")[0].firstChild.nodeValue
            urls.append(url)
            vtype, ext, _size = url_info(url)
            if not ext:
                ext = match1(url,r'\.(\w+?)\?')
            size += _size
        #sina's result does not contains content-type
        return urls, ext, size

def catfun_download(url, output_dir = '.', merge = True, info_only = False, **kwargs):
    # html = get_content(url)
    title = match1(get_content(url), r'<h1 class="title">(.+?)</h1>')
    vid = match1(url, r"v\d+/cat(\d+)")
    j = json.loads(get_content("http://www.catfun.tv/index.php?m=catfun&c=catfun_video&a=get_video&modelid=11&id={}".format(vid)))
    for item in j:
        if item["name"] != "\u672a\u547d\u540d1":
            t = title + "-" + item["name"]
        else:
            t = title
        if item["type"] == "tudou":
            tudou_download_by_id(item["vid"], title, output_dir, merge, info_only)

        else:
            urls, ext, size = parse_item(item)

            print_info(site_info, title, ext, size)
            if not info_only:
                download_urls(urls, t, ext, size, output_dir, merge=merge)

site_info = "CatFun.tv"
download = catfun_download
download_playlist = playlist_not_supported('catfun')
