#!/usr/bin/env python

from ..common import *
from ..extractor import VideoExtractor
from uuid import uuid4
from random import random,randint
import json
from math import floor
from zlib import decompress
import hashlib

'''
Changelog:
-> http://www.iqiyi.com/common/flashplayer/20150810/MainPlayer_5_2_26_c3_3_7_1.swf
   http://www.iqiyi.com/common/flashplayer/20150811/MainPlayer_5_2_26_c3_3_7_2.swf
   http://www.iqiyi.com/common/flashplayer/20150820/MainPlayer_5_2_27_2_c3_3_7_3.swf
    some small changes in Zombie.bite function

-> http://www.iqiyi.com/common/flashplayer/20150805/MainPlayer_5_2_26_c3_3_7.swf
    former key still works until 20150809
    In Zombie kcuf = [13, 3, 0, 15, 8, 2, 11, 7, 10, 1, 12, 9, 14, 6, 4, 5] ,which is construct in LogManager,CoreManager,impls.pub.setting,impls.pub.statistics,StageVideoManager
              thd create a array of ['2', 'd', 'f', 'e', '0', 'c', '5', '3', '8', 'b', '9', '6', 'a', '7', '4', '1']
-> http://www.iqiyi.com/common/flashplayer/20150710/MainPlayer_5_2_25_c3_3_5_1.swf

-> http://www.iqiyi.com/common/flashplayer/20150703/MainPlayer_5_2_24_1_c3_3_3.swf
    SingletonClass.ekam

-> http://www.iqiyi.com/common/flashplayer/20150618/MainPlayer_5_2_24_1_c3_3_2.swf
    In this version Z7elzzup.cexe,just use node.js to run this code(with some modification) and get innerkey.

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
    enc.append('3cba91f1453145438ac5e4f5983bc086')
    tm = str(randint(2000,4000))
    src = 'eknas'
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

def getDispathKey(rid):
    tp=")(*&^flash@#$%a"  #magic from swf
    time=json.loads(get_content("http://data.video.qiyi.com/t?tn="+str(random())))["t"]
    t=str(int(floor(int(time)/(10*60.0))))
    return hashlib.new("md5",bytes(t+tp+rid,"utf-8")).hexdigest()

class Iqiyi(VideoExtractor):
    name = "爱奇艺 (Iqiyi)"

    stream_types = [
        {'id': '4k', 'container': 'f4v', 'video_profile': '4K'},
        {'id': 'fullhd', 'container': 'f4v', 'video_profile': '全高清'},
        {'id': 'suprt-high', 'container': 'f4v', 'video_profile': '超高清'},
        {'id': 'super', 'container': 'f4v', 'video_profile': '超清'},
        {'id': 'high', 'container': 'f4v', 'video_profile': '高清'},
        {'id': 'standard', 'container': 'f4v', 'video_profile': '标清'},
        {'id': 'topspeed', 'container': 'f4v', 'video_profile': '最差'},
    ]

    stream_to_bid = {  '4k': 10, 'fullhd' : 5, 'suprt-high' : 4, 'super' : 3, 'high' : 2, 'standard' :1, 'topspeed' :96}

    stream_urls = {  '4k': [] , 'fullhd' : [], 'suprt-high' : [], 'super' : [], 'high' : [], 'standard' :[], 'topspeed' :[]}

    baseurl = ''

    gen_uid = ''
    def getVMS(self):
        #tm ->the flash run time for md5 usage
        #um -> vip 1 normal 0
        #authkey -> for password protected video ,replace '' with your password
        #puid user.passportid may empty?
        #TODO: support password protected video
        tvid, vid = self.vid
        tm, sc, src = mix(tvid)
        uid = self.gen_uid
        vmsreq='http://cache.video.qiyi.com/vms?key=fvip&src=1702633101b340d8917a69cf8a4b8c7' +\
                "&tvId="+tvid+"&vid="+vid+"&vinfo=1&tm="+tm+\
                "&enc="+sc+\
                "&qyid="+uid+"&tn="+str(random()) +"&um=1" +\
                "&authkey="+hashlib.new('md5',bytes(''+str(tm)+tvid,'utf-8')).hexdigest()
        return json.loads(get_content(vmsreq))



    def prepare(self, **kwargs):
        assert self.url or self.vid

        if self.url and not self.vid:
            html = get_html(self.url)
            tvid = r1(r'data-player-tvid="([^"]+)"', html) or r1(r'tvid=([^&]+)', self.url)
            videoid = r1(r'data-player-videoid="([^"]+)"', html) or r1(r'vid=([^&]+)', self.url)
            self.vid = (tvid, videoid)

        self.gen_uid=uuid4().hex
        info = self.getVMS()

        assert info["code"] == "A000000"

        self.title = info["data"]["vi"]["vn"]

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

        vs = info["data"]["vp"]["tkl"][0]["vs"]
        self.baseurl=info["data"]["vp"]["du"].split("/")

        for stream in self.stream_types:
            for i in vs:
                if self.stream_to_bid[stream['id']] == i['bid']:
                    video_links=i["fs"] #now in i["flvs"] not in i["fs"]
                    if not i["fs"][0]["l"].startswith("/"):
                        tmp = getVrsEncodeCode(i["fs"][0]["l"])
                        if tmp.endswith('mp4'):
                             video_links = i["flvs"]
                    self.stream_urls[stream['id']] = video_links
                    size = 0
                    for l in video_links:
                        size += l['b']
                    self.streams[stream['id']] = {'container': stream['container'], 'video_profile': stream['video_profile'], 'size' : size}
                    break

    def extract(self, **kwargs):
        if 'stream_id' in kwargs and kwargs['stream_id']:
            # Extract the stream
            stream_id = kwargs['stream_id']

            if stream_id not in self.streams:
                log.e('[Error] Invalid video format.')
                log.e('Run \'-i\' command with no specific video format to view all available formats.')
                exit(2)
        else:
            # Extract stream with the best quality
            stream_id = self.streams_sorted[0]['id']

        urls=[]
        for i in self.stream_urls[stream_id]:
            vlink=i["l"]
            if not vlink.startswith("/"):
                #vlink is encode
                vlink=getVrsEncodeCode(vlink)
            key=getDispathKey(vlink.split("/")[-1].split(".")[0])
            baseurl = [x for x in self.baseurl]
            baseurl.insert(-1,key)
            url="/".join(baseurl)+vlink+'?su='+self.gen_uid+'&qyid='+uuid4().hex+'&client=&z=&bt=&ct=&tn='+str(randint(10000,20000))
            urls.append(json.loads(get_content(url))["l"])
        #download should be complete in 10 minutes
        #because the url is generated before start downloading
        #and the key may be expired after 10 minutes
        self.streams[stream_id]['src'] = urls

site = Iqiyi()
download = site.download_by_url
iqiyi_download_by_vid = site.download_by_vid
download_playlist = playlist_not_supported('iqiyi')
