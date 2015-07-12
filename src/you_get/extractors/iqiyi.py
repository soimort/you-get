#!/usr/bin/env python

__all__ = ['iqiyi_download']

from ..common import *
from uuid import uuid4
from random import random,randint
import json
from math import floor
from zlib import decompress
import hashlib

'''
Changelog:
-> http://www.iqiyi.com/common/flashplayer/20150710/MainPlayer_5_2_25_c3_3_5_1.swf

-> http://www.iqiyi.com/common/flashplayer/20150703/MainPlayer_5_2_24_1_c3_3_3.swf
    SingletonClass.ekam

-> http://www.iqiyi.com/common/flashplayer/20150618/MainPlayer_5_2_24_1_c3_3_2.swf
    In this version Z7elzzup.cexe,just use node.js to run this code(with some modification) and get innerkey.

-> http://www.iqiyi.com/common/flashplayer/20150612/MainPlayer_5_2_23_1_c3_2_6_5.swf
    In this version do not directly use enc key
    gen enc key (so called sc ) in DMEmagelzzup.mix(tvid) -> (tm->getTimer(),src='hsalf',sc)
    encrypy alogrithm is md5(DMEmagelzzup.mix.genInnerKey +tm+tvid)
    how to gen genInnerKey ,can see first 3 lin in mix function in this file
'''

'''
com.qiyi.player.core.model.def.DefinitonEnum
bid meaning for quality
0 none
1 standard
2 high
3 super
4 suprt-high
5 fullhd
10 4k
96 topspeed

'''

def mix(tvid):
    enc = []
    enc.append('341c0055ad1d4e798c2b784d9dbed29f')
    tm = str(randint(2000,4000))
    src = 'hsalf'
    enc.append(str(tm))
    enc.append(tvid)
    sc = hashlib.new('md5',bytes("".join(enc),'utf-8')).hexdigest()
    return tm,sc,src

def getVRSXORCode(arg1,arg2):
    loc3=arg2 %3
    if loc3 == 1:
        return arg1^121
    if loc3 == 2:
        return arg1^72
    return arg1^103


def getVrsEncodeCode(vlink):
    loc6=0
    loc2=''
    loc3=vlink.split("-")
    loc4=len(loc3)
    # loc5=loc4-1
    for i in range(loc4-1,-1,-1):
        loc6=getVRSXORCode(int(loc3[loc4-i-1],16),i)
        loc2+=chr(loc6)
    return loc2[::-1]

def getVMS(tvid,vid,uid):
    #tm ->the flash run time for md5 usage
    #um -> vip 1 normal 0
    #authkey -> for password protected video ,replace '' with your password
    #puid user.passportid may empty?
    #TODO: support password protected video
    tm,sc,src = mix(tvid)
    vmsreq='http://cache.video.qiyi.com/vms?key=fvip&src=1702633101b340d8917a69cf8a4b8c7' +\
                "&tvId="+tvid+"&vid="+vid+"&vinfo=1&tm="+tm+\
                "&enc="+sc+\
                "&qyid="+uid+"&tn="+str(random()) +"&um=0" +\
                "&authkey="+hashlib.new('md5',bytes(''+str(tm)+tvid,'utf-8')).hexdigest()
    return json.loads(get_content(vmsreq))

def getDispathKey(rid):
    tp=")(*&^flash@#$%a"  #magic from swf
    time=json.loads(get_content("http://data.video.qiyi.com/t?tn="+str(random())))["t"]
    t=str(int(floor(int(time)/(10*60.0))))
    return hashlib.new("md5",bytes(t+tp+rid,"utf-8")).hexdigest()


def iqiyi_download(url, output_dir = '.', merge = True, info_only = False):
    gen_uid=uuid4().hex

    html = get_html(url)

    tvid = r1(r'data-player-tvid="([^"]+)"', html) or r1(r'tvid=([^&]+)', url)
    videoid = r1(r'data-player-videoid="([^"]+)"', html) or r1(r'vid=([^&]+)', url)

    assert tvid
    assert videoid

    info = getVMS(tvid, videoid, gen_uid)

    assert info["code"] == "A000000"

    title = info["data"]["vi"]["vn"]

    # data.vp = json.data.vp
    #  data.vi = json.data.vi
    #  data.f4v = json.data.f4v
    # if movieIsMember data.vp = json.data.np

    #for highest qualities
    #for http://www.iqiyi.com/v_19rrmmz5yw.html  not vp -> np
    try:
        if info["data"]['vp']["tkl"]=='' :
            raise ValueError
    except:
        log.e("[Error] Do not support for iQIYI VIP video.")
        exit(-1)

    bid=0
    for i in info["data"]["vp"]["tkl"][0]["vs"]:
        if int(i["bid"])<=10 and int(i["bid"])>=bid:
            bid=int(i["bid"])

            video_links=i["fs"] #now in i["flvs"] not in i["fs"]
            if not i["fs"][0]["l"].startswith("/"):
                tmp = getVrsEncodeCode(i["fs"][0]["l"])
                if tmp.endswith('mp4'):
                     video_links = i["flvs"]


    urls=[]
    size=0
    for i in video_links:
        vlink=i["l"]
        if not vlink.startswith("/"):
            #vlink is encode
            vlink=getVrsEncodeCode(vlink)
        key=getDispathKey(vlink.split("/")[-1].split(".")[0])
        size+=i["b"]
        baseurl=info["data"]["vp"]["du"].split("/")
        baseurl.insert(-1,key)
        url="/".join(baseurl)+vlink+'?su='+gen_uid+'&qyid='+uuid4().hex+'&client=&z=&bt=&ct=&tn='+str(randint(10000,20000))
        urls.append(json.loads(get_content(url))["l"])
    #download should be complete in 10 minutes
    #because the url is generated before start downloading
    #and the key may be expired after 10 minutes
    print_info(site_info, title, 'flv', size)
    if not info_only:
        download_urls(urls, title, 'flv', size, output_dir = output_dir, merge = merge)

site_info = "iQIYI.com"
download = iqiyi_download
download_playlist = playlist_not_supported('iqiyi')
