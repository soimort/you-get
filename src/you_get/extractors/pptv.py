#!/usr/bin/env python

__all__ = ['pptv_download', 'pptv_download_by_id']

from ..common import *

import re
import time
import urllib
from random import random
import xml.etree.ElementTree as ET
from urllib import request
from multiprocessing.dummy import Pool 

#Thanks to FFDEC and showmycode.com
#decompile Player4Player2.swf and VodCore.swf
#key point
# in Player4player2.swf
#cn.pplive.player.model.VodPlayProxy -> playUrl #to get xml info
#cn.pplive.player.controller.VodPlayCommand -> execute #parse xml info
#cn.pplive.player.view.components.VodP2PPlayer ->addNetStream #send info to the kernel(aka vodcore.swf)
   #constructKey in Utils
#in player4player2.swf version 3.3.0.9
#cn.pplive.player.model.VodPlayProxy -> ppllive.core.proxy.VodPlayProxy
#and etc
# go into vodcore.swf
# com.pplive.play.Playinfo -> constructCdnURL

class PPTVUrlGenerator():
    def __init__(self,rid,numbers,k,refer_url):
        #self.urls = urls
        self.cur = 0
        self.length = len(numbers)
        self.refer_url = refer_url
        self.rid = rid
        self.numbers = numbers
        self.k = k

    def __iter__(self):
        return self

    def __next__(self):
        if self.cur == self.length:
            raise StopIteration
        url= "http://ccf.pptv.com/{}/{}?key={}&fpp.ver=1.3.0.15&k={}&type=web.fpp".format(self.numbers[self.cur],self.rid,constructKey(int(time.time()-60)),self.k)
        real_url = request.urlopen(request.Request(url,headers={'Referer':self.refer_url})).geturl()
        self.cur += 1 
        return real_url

    def __len__(self):
        return self.length

    def __str__(self):
        return str([i for i in self])


def constructKey(arg):

    def str2hex(s):
        r=""
        for i in s[:8]:
            t=hex(ord(i))[2:]
            if len(t)==1:
                t="0"+t
            r+=t
        for i in range(16):
            r+=hex(int(15*random()))[2:]
        return r

    #ABANDONED  Because SERVER_KEY is static
    def getkey(s):
        #returns 1896220160
        l2=[i for i in s]
        l4=0
        l3=0
        while l4<len(l2):
            l5=l2[l4]
            l6=ord(l5)
            l7=l6<<((l4%4)*8)
            l3=l3^l7
            l4+=1
        return l3
        pass
    
    def rot(k,b): ##>>> in as3
        if k>=0:
            return k>>b
        elif k<0:
            return (2**32+k)>>b
        pass
     
    def lot(k,b):
        return (k<<b)%(2**32)

    #WTF?
    def encrypt(arg1,arg2):
        delta=2654435769
        l3=16;
        l4=getkey(arg2)  #1896220160
        l8=[i for i in arg1]
        l10=l4;
        l9=[i for i in arg2]
        l5=lot(l10,8)|rot(l10,24)#101056625
        # assert l5==101056625
        l6=lot(l10,16)|rot(l10,16)#100692230
        # assert 100692230==l6
        l7=lot(l10,24)|rot(l10,8)
        # assert 7407110==l7
        l11=""
        l12=0
        l13=ord(l8[l12])<<0
        l14=ord(l8[l12+1])<<8
        l15=ord(l8[l12+2])<<16
        l16=ord(l8[l12+3])<<24
        l17=ord(l8[l12+4])<<0
        l18=ord(l8[l12+5])<<8
        l19=ord(l8[l12+6])<<16
        l20=ord(l8[l12+7])<<24
     
        l21=(((0|l13)|l14)|l15)|l16
        l22=(((0|l17)|l18)|l19)|l20
     
        l23=0
        l24=0
        while l24<32:
            l23=(l23+delta)%(2**32)
            l33=(lot(l22,4)+l4)%(2**32)
            l34=(l22+l23)%(2**32)
            l35=(rot(l22,5)+l5)%(2**32)
            l36=(l33^l34)^l35
            l21=(l21+l36)%(2**32)
            l37=(lot(l21,4)+l6)%(2**32)
            l38=(l21+l23)%(2**32)
            l39=(rot(l21,5))%(2**32)
            l40=(l39+l7)%(2**32)
            l41=((l37^l38)%(2**32)^l40)%(2**32)
            l22=(l22+l41)%(2**32)
     
            l24+=1
     
        l11+=chr(rot(l21,0)&0xff)
        l11+=chr(rot(l21,8)&0xff)
        l11+=chr(rot(l21,16)&0xff)
        l11+=chr(rot(l21,24)&0xff)
        l11+=chr(rot(l22,0)&0xff)
        l11+=chr(rot(l22,8)&0xff)
        l11+=chr(rot(l22,16)&0xff)
        l11+=chr(rot(l22,24)&0xff)
     
        return l11        
            

    loc1=hex(int(arg))[2:]+(16-len(hex(int(arg))[2:]))*"\x00"
    SERVER_KEY="qqqqqww"+"\x00"*9
    res=encrypt(loc1,SERVER_KEY)
    return str2hex(res)





#quality level
#level bitrate
# 0     336 
# 1     452
# 2     782
# 3     1764  ->for vip
# 4     6144  ->for vip 

def pptv_download_by_id(cid,refer_url, output_dir = '.', merge = True, info_only = False ,**kwargs):
    #xml api version update to 4 @2015/01/31
    #modify xmlreq@2015/05/14  for http://player.pplive.cn/ikan/3.4.0.12/player4player2.swf 
    xmlurl = 'http://web-play.pptv.com/webplay3-0-%s.xml?zone=8&pid=5701&username=&salt=pv&o=0&referer=&param=type%%3Dweb.fpp%%26userType%%3D0%%26o%%3D0&version=4&type=web.fpp&r=%d&pageUrl=%s' % (cid,time.time()/1000,refer_url)
    xmlstr = get_html(xmlurl)
    xml = ET.fromstring(xmlstr)

    stream_id = '2' #default vip level may have some error?
    support_stream_id = sorted([i.get("ft") for i in xml.findall("./channel/file/item")])
    #support_stream_id = sorted([i.get("ft") for i in xml.findall("./channel/file/item[@vip='0']")])

    if "stream_id" in kwargs and kwargs["stream_id"] in support_stream_id:
        stream_id = kwargs["stream_id"]
    else:
        print("Current Video Supports:")
        for i in support_stream_id:
            bitrate = xml.find("./channel/file/item[@ft='{}']".format(i)).get('bitrate')
            filesize = int(xml.find("./channel/file/item[@ft='{}']".format(i)).get('filesize'))
            vip = int(xml.find("./channel/file/item[@ft='{}']".format(i)).get('vip'))
            print("\t--format",i,"<URL>:","bitrate:",bitrate,"kbps","size:","%.2f"% (filesize/ 1024.0 /1024.0),"MB", "<---default" if int(i) == int(stream_id) else '')


    item = xml.find("./channel/file/item[@ft='{}']".format(stream_id))
    assert item!=None 
    dt = xml.find("./dt[@ft='{}']".format(stream_id))
    assert dt!=None
    dragdata = xml.find("./dragdata[@ft='{}']".format(stream_id))
    assert dragdata!=None

    host = dt.find('sh').text
    k = dt.find('key').text
    rid = item.get('rid')
    assert rid.endswith('.mp4')
    title = xml.find("./channel").get('nm')

    numbers = [ i.get('no') for i in dragdata.findall('sgm')]
    type_ = "web.fpp"
    #urls=[ "http://ccf.pptv.com/{}/{}?key={}&fpp.ver=1.3.0.15&k={}&type={}".format(i,rid,key,k,type_)  for i in numbers]


    #def convertUrl(url):
    #    res = request.urlopen(request.Request(url,headers={'Referer':refer_url},method='HEAD'))
    #    return (int(res.headers.get('content-length',0)),res.geturl())
    
    #threads = Pool(10) 
    #results = threads.map(convertUrl,urls)
    #threads.close()
    #threads.join()

    #size_list ,real_urls = zip(*results)
    #total_size = sum(size_list) 
    #print(real_urls)
    
    total_size = sum(map(int, [ i.get('fs') for i in dragdata.findall('sgm')])) #reliable 

    print_info(site_info, title, 'mp4', total_size)

    if not info_only:
        try:
            #accept-encoding = *  is a workaround ,cause server of pptv may not return content-length when accept-encoding is special point to some zip algorithm 
            download_urls(PPTVUrlGenerator(rid,numbers,k,refer_url), title, 'mp4', total_size, output_dir = output_dir, merge = merge,  faker = {'Referer':refer_url,'Accept-Encoding':'*'})
        except urllib.error.HTTPError as e:
            print(e.message)
            # pptv_download_by_id(cid, refer_url, output_dir = output_dir, merge = merge, info_only = info_only,**kwargs)
            pass

def pptv_download(url, output_dir = '.', merge = True, info_only = False , **kwargs):
    assert re.match(r'http://v.pptv.com/show/(\w+)\.html', url)
    html = get_html(url)
    cid = r1(r'webcfg\s*=\s*{"id":\s*(\d+)', html)
    assert cid
    pptv_download_by_id(cid, url ,output_dir = output_dir, merge = merge, info_only = info_only,**kwargs)

site_info = "PPTV.com"
download = pptv_download
download_playlist = playlist_not_supported('pptv')

