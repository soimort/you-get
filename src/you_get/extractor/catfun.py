#!/usr/bin/env python

__all__ = ['catfun_download']

from ..common import *

def parse_item(item):
    if item["type"]=="youku":
        page=get_content("http://www.catfun.tv/index.php?m=catfun&c=catfun_video&a=get_youku_video_info&youku_id="+item["vid"])
        pass

    elif item["type"]=="qq":
        page=get_content("http://www.catfun.tv/index.php?m=catfun&c=catfun_video&a=get_qq_video_info&qq_id="+item["vid"])

        pass

    elif item["type"]=="sina":
        page=get_content("http://www.catfun.tv/index.php?m=catfun&c=catfun_video&a=get_sina_video_info&sina_id=" + item["vid"])
        pass

    elif item["type"]=="tudou_iid":
        page=get_content("http://www.tudou.com/outplay/goto/getItemSegs.action?iid="+item["vid"])
        pass

    elif item["type"]=="tudou":
        page=get_content("http://www.tudou.com/outplay/goto/getItemSegs.action?iid="+match1(item["vid"],r"iid: ([0-9]*)"))     
        pass


def catfun_download(url, output_dir = '.', merge = True, info_only = False):
    # html=get_content(url)
    title=match1(get_content(url),r'<h1 class="title">(.+?)</h1>')
    vid=match1(url,r"v\d+/cat(\d+)")
    j=json.loads(get_content("http://www.catfun.tv/index.php?m=catfun&c=catfun_video&a=get_video&modelid=11&id={}".format(vid)))
    for item in j:
        parse_item(item)


site_info = "catfun.com"
download = catfun_download
download_playlist = playlist_not_supported('catfun')