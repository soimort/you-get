#!/usr/bin/env python

from ..common import *
from ..common import print_more_compatible as print
from ..extractor import VideoExtractor
from ..util import log
from .. import json_output

from uuid import uuid4
from random import random,randint
import json
from math import floor
from zlib import decompress
import hashlib
import time

'''
Changelog:
-> http://www.iqiyi.com/common/flashplayer/20150916/MainPlayer_5_2_28_c3_3_7_4.swf
   use @fffonion 's method in #617.
   Add trace AVM(asasm) code in Iqiyi's encode function where the salt is put into the encode array and reassemble by RABCDasm(or WinRABCDasm),then use Fiddler to response modified file to replace the src file with its AutoResponder function ,set browser Fiddler proxy and play with !debug version! Flash Player ,finially get result in flashlog.txt(its location can be easily found in search engine).
   Code Like (without letters after #comment:),it just do the job : trace("{IQIYI_SALT}:"+salt_array.join(""))
   ```(Position After getTimer)
     findpropstrict      QName(PackageNamespace(""), "trace")
     pushstring          "{IQIYI_SALT}:" #comment for you to locate the salt
     getscopeobject      1
     getslot             17 #comment: 17 is the salt slots number defined in code
     pushstring          ""
     callproperty        QName(Namespace("http://adobe.com/AS3/2006/builtin"), "join"), 1
     add
     callpropvoid        QName(PackageNamespace(""), "trace"), 1
   ```

-> http://www.iqiyi.com/common/flashplayer/20150820/MainPlayer_5_2_27_2_c3_3_7_3.swf
    some small changes in Zombie.bite function

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
'''
def mix(tvid):
    salt = '4a1caba4b4465345366f28da7c117d20'
    tm = str(randint(2000,4000))
    sc = hashlib.new('md5', bytes(salt + tm + tvid, 'utf-8')).hexdigest()
    return tm, sc, 'eknas'

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
'''
def getVMS(tvid, vid):
    t = int(time.time() * 1000)
    src = '76f90cbd92f94a2e925d83e8ccd22cb7'
    key = 'd5fb4bd9d50c4be6948c97edd7254b0e'
    sc = hashlib.new('md5', bytes(str(t) + key  + vid, 'utf-8')).hexdigest()
    vmsreq= url = 'http://cache.m.iqiyi.com/tmts/{0}/{1}/?t={2}&sc={3}&src={4}'.format(tvid,vid,t,sc,src)
    return json.loads(get_content(vmsreq))

class Iqiyi(VideoExtractor):
    name = "爱奇艺 (Iqiyi)"

    stream_types = [
        {'id': '4k', 'container': 'm3u8', 'video_profile': '4k'},
        {'id': 'BD', 'container': 'm3u8', 'video_profile': '1080p'},
        {'id': 'TD', 'container': 'm3u8', 'video_profile': '720p'},
        {'id': 'TD_H265', 'container': 'm3u8', 'video_profile': '720p H265'},
        {'id': 'HD', 'container': 'm3u8', 'video_profile': '540p'},
        {'id': 'HD_H265', 'container': 'm3u8', 'video_profile': '540p H265'},
        {'id': 'SD', 'container': 'm3u8', 'video_profile': '360p'},
        {'id': 'LD', 'container': 'm3u8', 'video_profile': '210p'},
    ]
    '''
    supported_stream_types = [ 'high', 'standard']


    stream_to_bid = {  '4k': 10, 'fullhd' : 5, 'suprt-high' : 4, 'super' : 3, 'high' : 2, 'standard' :1, 'topspeed' :96}
    '''
    ids = ['4k','BD', 'TD', 'HD', 'SD', 'LD']
    vd_2_id = {10: '4k', 19: '4k', 5:'BD', 18: 'BD', 21: 'HD_H265', 2: 'HD', 4: 'TD', 17: 'TD_H265', 96: 'LD', 1: 'SD', 14: 'TD'}
    id_2_profile = {'4k':'4k', 'BD': '1080p','TD': '720p', 'HD': '540p', 'SD': '360p', 'LD': '210p', 'HD_H265': '540p H265', 'TD_H265': '720p H265'}



    def download_playlist_by_url(self, url, **kwargs):
        self.url = url

        video_page = get_content(url)
        videos = set(re.findall(r'<a href="(?=https?:)?(//www\.iqiyi\.com/v_[^"]+)"', video_page))

        for video in videos:
            self.__class__().download_by_url('https:' + video, **kwargs)

    def prepare(self, **kwargs):
        assert self.url or self.vid

        if self.url and not self.vid:
            html = get_html(self.url)
            tvid = r1(r'#curid=(.+)_', self.url) or \
                   r1(r'tvid=([^&]+)', self.url) or \
                   r1(r'data-player-tvid="([^"]+)"', html) or r1(r'tv(?:i|I)d=(.+?)\&', html) or r1(r'param\[\'tvid\'\]\s*=\s*"(.+?)"', html)
            videoid = r1(r'#curid=.+_(.*)$', self.url) or \
                      r1(r'vid=([^&]+)', self.url) or \
                      r1(r'data-player-videoid="([^"]+)"', html) or r1(r'vid=(.+?)\&', html) or r1(r'param\[\'vid\'\]\s*=\s*"(.+?)"', html)
            self.vid = (tvid, videoid)
            info_u = 'http://pcw-api.iqiyi.com/video/video/playervideoinfo?tvid=' + tvid
            json_res = get_content(info_u)
            self.title = json.loads(json_res)['data']['vn']
        tvid, videoid = self.vid
        info = getVMS(tvid, videoid)
        assert info['code'] == 'A00000', "can't play this video"

        for stream in info['data']['vidl']:
            try:
                stream_id = self.vd_2_id[stream['vd']]
                if stream_id in self.stream_types:
                    continue
                stream_profile = self.id_2_profile[stream_id]
                self.streams[stream_id] = {'video_profile': stream_profile, 'container': 'm3u8', 'src': [stream['m3u']], 'size' : 0, 'm3u8_url': stream['m3u']}
            except Exception as e:
                log.i("vd: {} is not handled".format(stream['vd']))
                log.i("info is {}".format(stream))


    def download(self, **kwargs):
        """Override the original one
        Ugly ugly dirty hack"""
        if 'json_output' in kwargs and kwargs['json_output']:
            json_output.output(self)
        elif 'info_only' in kwargs and kwargs['info_only']:
            if 'stream_id' in kwargs and kwargs['stream_id']:
                # Display the stream
                stream_id = kwargs['stream_id']
                if 'index' not in kwargs:
                    self.p(stream_id)
                else:
                    self.p_i(stream_id)
            else:
                # Display all available streams
                if 'index' not in kwargs:
                    self.p([])
                else:
                    stream_id = self.streams_sorted[0]['id'] if 'id' in self.streams_sorted[0] else self.streams_sorted[0]['itag']
                    self.p_i(stream_id)

        else:
            if 'stream_id' in kwargs and kwargs['stream_id']:
                # Download the stream
                stream_id = kwargs['stream_id']
            else:
                # Download stream with the best quality
                stream_id = self.streams_sorted[0]['id'] if 'id' in self.streams_sorted[0] else self.streams_sorted[0]['itag']

            if 'index' not in kwargs:
                self.p(stream_id)
            else:
                self.p_i(stream_id)

            if stream_id in self.streams:
                urls = self.streams[stream_id]['src']
                ext = self.streams[stream_id]['container']
                total_size = self.streams[stream_id]['size']
            else:
                urls = self.dash_streams[stream_id]['src']
                ext = self.dash_streams[stream_id]['container']
                total_size = self.dash_streams[stream_id]['size']

            if not urls:
                log.wtf('[Failed] Cannot extract video source.')
            # For legacy main()

            #Here's the change!!
            download_url_ffmpeg(urls[0], self.title, 'mp4', output_dir=kwargs['output_dir'], merge=kwargs['merge'], stream=False)

            if not kwargs['caption']:
                print('Skipping captions.')
                return
            for lang in self.caption_tracks:
                filename = '%s.%s.srt' % (get_filename(self.title), lang)
                print('Saving %s ... ' % filename, end="", flush=True)
                srt = self.caption_tracks[lang]
                with open(os.path.join(kwargs['output_dir'], filename),
                          'w', encoding='utf-8') as x:
                    x.write(srt)
                print('Done.')

'''
        if info["code"] != "A000000":
            log.e("[error] outdated iQIYI key")
            log.wtf("is your you-get up-to-date?")

        self.title = info["data"]["vi"]["vn"]
        self.title = self.title.replace('\u200b', '')

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
'''

site = Iqiyi()
download = site.download_by_url
iqiyi_download_by_vid = site.download_by_vid
download_playlist = site.download_playlist_by_url
