#!/usr/bin/env python

__all__ = ['pptv_download', 'pptv_download_by_id']

from ..common import *

import re
import time
import urllib
from random import random


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


def pptv_download_by_id(id, title = None, output_dir = '.', merge = True, info_only = False):
    xml = get_html('http://web-play.pptv.com/webplay3-0-%s.xml?type=web.fpp' % id)
    #vt=3 means vod mode vt=5 means live mode
    host = r1(r'<sh>([^<>]+)</sh>', xml)
    k = r1(r'<key expire=[^<>]+>([^<>]+)</key>', xml)
    rid = r1(r'rid="([^"]+)"', xml)
    title = r1(r'nm="([^"]+)"', xml)

    st=r1(r'<st>([^<>]+)</st>',xml)[:-4]
    st=time.mktime(time.strptime(st))*1000-60*1000-time.time()*1000
    st+=time.time()*1000
    st=st/1000

    key=constructKey(st)

    pieces = re.findall('<sgm no="(\d+)"[^<>]+fs="(\d+)"', xml)
    numbers, fs = zip(*pieces)
    urls=["http://{}/{}/{}?key={}&fpp.ver=1.3.0.4&k={}&type=web.fpp".format(host,i,rid,key,k) for i in range(max(map(int,numbers))+1)]

    total_size = sum(map(int, fs))
    assert rid.endswith('.mp4')
    print_info(site_info, title, 'mp4', total_size)

    if not info_only:
        try:
            download_urls(urls, title, 'mp4', total_size, output_dir = output_dir, merge = merge)
        except urllib.error.HTTPError:
            #for key expired
            pptv_download_by_id(id, output_dir = output_dir, merge = merge, info_only = info_only)

def pptv_download(url, output_dir = '.', merge = True, info_only = False, **kwargs):
    assert re.match(r'http://v.pptv.com/show/(\w+)\.html$', url)
    html = get_html(url)
    id = r1(r'webcfg\s*=\s*{"id":\s*(\d+)', html)
    assert id
    pptv_download_by_id(id, output_dir = output_dir, merge = merge, info_only = info_only)

site_info = "PPTV.com"
download = pptv_download
download_playlist = playlist_not_supported('pptv')
