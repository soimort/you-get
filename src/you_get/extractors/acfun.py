#!/usr/bin/env python

__all__ = ['acfun_download']

from ..common import *

from .letv import letvcloud_download_by_vu
from .qq import qq_download_by_vid
from .sina import sina_download_by_vid
from .tudou import tudou_download_by_iid
from .youku import youku_download_by_vid

import json, re

def get_srt_json(id):
    # url = 'http://comment.acfun.tv/%s.json' % id
    url = 'http://static.comment.acfun.mm111.net/%s' %id
    return get_html(url)

def get_srt_lock_json(id):
    url = 'http://comment.acfun.tv/%s_lock.json' % id
    return get_html(url)

def acfun_download_by_vid(vid, title=None, output_dir='.', merge=True, info_only=False, **kwargs):
    info = json.loads(get_html('http://www.acfun.tv/video/getVideo.aspx?id=' + vid))
    sourceType = info['sourceType']
    sourceId = info['sourceId']
    # danmakuId = info['danmakuId']
    if sourceType == 'sina':
        sina_download_by_vid(sourceId, title, output_dir=output_dir, merge=merge, info_only=info_only)
    elif sourceType == 'youku':
        youku_download_by_vid(sourceId, title=title, output_dir=output_dir, merge=merge, info_only=info_only)
    elif sourceType == 'tudou':
        tudou_download_by_iid(sourceId, title, output_dir=output_dir, merge=merge, info_only=info_only)
    elif sourceType == 'qq':
        qq_download_by_vid(sourceId, title, output_dir=output_dir, merge=merge, info_only=info_only)
    elif sourceType == 'letv':
        letvcloud_download_by_vu(sourceId, '2d8c027396', title, output_dir=output_dir, merge=merge, info_only=info_only)
    else:
        raise NotImplementedError(sourceType)

    if not info_only:
        title = get_filename(title)
        try:
            print('Downloading %s ...\n' % (title + '.cmt.json'))
            cmt = get_srt_json(vid)
            with open(os.path.join(output_dir, title + '.cmt.json'), 'w') as x:
                x.write(cmt)
            # print('Downloading %s ...\n' % (title + '.cmt_lock.json'))
            # cmt = get_srt_lock_json(danmakuId)
            # with open(os.path.join(output_dir, title + '.cmt_lock.json'), 'w') as x:
            #     x.write(cmt)
        except:
            pass



# decompile from player swf
# protected static const VIDEO_PARSE_API:String = "http://jiexi.acfun.info/index.php?vid=";
# protected static var VIDEO_RATES_CODE:Array = ["C40","C30","C20","C10"];
# public static var VIDEO_RATES_STRING:Array = ["原画","超清","高清","流畅"];
# Sometimes may find C80 but size smaller than C30 


#def acfun_download_by_vid(vid, title=None, output_dir='.', merge=True, info_only=False ,**kwargs):
    ###api example http://jiexi.acfun.info/index.php?vid=1122870
    #info = json.loads(get_content("http://jiexi.acfun.info/index.php?vid={}".format(vid)))
    #assert info["code"] == 200
    #assert info["success"] == True

    #support_types = sorted(info["result"].keys(),key= lambda i: int(i[1:]))

    #stream_id = None
    #if "stream_id" in kwargs and kwargs["stream_id"] in support_types:
        #stream_id = kwargs["stream_id"]
    #else:
        #print("Current Video Supports:")
        #for i in support_types:
            #if info["result"][i]["totalbytes"] != 0:
                #print("\t--format",i,"<URL>:",info["result"][i]["quality"],"size:","%.2f"% (info["result"][i]["totalbytes"] / 1024.0 /1024.0),"MB")
            #else:
                #print("\t--format",i,"<URL>:",info["result"][i]["quality"])
        ##because C80 is not the best
        #if "C80" not in support_types:
            #stream_id = support_types[-1]
        #else:
            #stream_id = support_types[-2]

    #urls = [None] * len(info["result"][stream_id]["files"])
    #for i in info["result"][stream_id]["files"]:
        #urls[i["no"]] = i["url"]
    #ext = info["result"][stream_id]["files"][0]["type"]
    #size = 0
    #for i in urls:
        #_, _, tmp =url_info(i)
        #size +=tmp
    #print_info(site_info, title, ext, size)
    #print("Format:    ",stream_id)
    #print()

    #if not info_only:
        #download_urls(urls, title, ext, size, output_dir = output_dir, merge = merge)
        #title = get_filename(title)
        #try:
            #print('Downloading %s ...\n' % (title + '.cmt.json'))
            #cmt = get_srt_json(vid)
            #with open(os.path.join(output_dir, title + '.cmt.json'), 'w') as x:
                #x.write(cmt)
        #except:
            #pass

def acfun_download(url, output_dir='.', merge=True, info_only=False, **kwargs):
    assert re.match(r'http://[^\.]+.acfun.[^\.]+/\D/\D\D(\d+)', url)
    html = get_html(url)

    title = r1(r'<h1 id="txt-title-view">([^<>]+)<', html)
    title = unescape_html(title)
    title = escape_file_path(title)
    assert title

    videos = re.findall("data-vid=\"(\d+)\".*href=\"[^\"]+\".*title=\"([^\"]+)\"", html)
    if videos is not None:
        for video in videos:
            p_vid = video[0]
            p_title = title + " - " + video[1]
            acfun_download_by_vid(p_vid, p_title, output_dir=output_dir, merge=merge, info_only=info_only ,**kwargs)
    else:
        # Useless - to be removed?
        id = r1(r"src=\"/newflvplayer/player.*id=(\d+)", html)
        sina_download_by_vid(id, title, output_dir=output_dir, merge=merge, info_only=info_only)

site_info = "AcFun.tv"
download = acfun_download
download_playlist = playlist_not_supported('acfun')
