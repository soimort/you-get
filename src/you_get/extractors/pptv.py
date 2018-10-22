#!/usr/bin/env python

#__all__ = ['pptv_download', 'pptv_download_by_id']

from ..common import *
from ..extractor import VideoExtractor

import re
import time
import urllib
import random
import binascii
from xml.dom.minidom import parseString


def lshift(a, b):
    return (a << b) & 0xffffffff
def rshift(a, b):
    if a >= 0:
        return a >> b
    return (0x100000000 + a) >> b

def le32_pack(b_str):
    result = 0
    result |= b_str[0]
    result |= (b_str[1] << 8)
    result |= (b_str[2] << 16)
    result |= (b_str[3] << 24)
    return result

def tea_core(data, key_seg):
    delta = 2654435769

    d0 = le32_pack(data[:4])
    d1 = le32_pack(data[4:8])

    sum_ = 0
    for rnd in range(32):
        sum_ = (sum_ + delta) & 0xffffffff
        p1 = (lshift(d1, 4) + key_seg[0]) & 0xffffffff
        p2 = (d1 + sum_) & 0xffffffff
        p3 = (rshift(d1, 5) + key_seg[1]) & 0xffffffff

        mid_p = p1 ^ p2 ^ p3
        d0 = (d0 + mid_p) & 0xffffffff

        p4 = (lshift(d0, 4) + key_seg[2]) & 0xffffffff
        p5 = (d0 + sum_) & 0xffffffff
        p6 = (rshift(d0, 5) + key_seg[3]) & 0xffffffff

        mid_p = p4 ^ p5 ^ p6
        d1 = (d1 + mid_p) & 0xffffffff

    return bytes(unpack_le32(d0) + unpack_le32(d1))

def ran_hex(size):
    result = []
    for i in range(size):
        result.append(hex(int(15 * random.random()))[2:])
    return ''.join(result)

def zpad(b_str, size):
    size_diff = size - len(b_str)
    return b_str + bytes(size_diff)

def gen_key(t):
    key_seg = [1896220160,101056625, 100692230, 7407110]
    t_s = hex(int(t))[2:].encode('utf8')
    input_data = zpad(t_s, 16)
    out = tea_core(input_data, key_seg)
    return binascii.hexlify(out[:8]).decode('utf8') + ran_hex(16)

def unpack_le32(i32):
    result = []
    result.append(i32 & 0xff)
    i32 = rshift(i32, 8)
    result.append(i32 & 0xff)
    i32 = rshift(i32, 8)
    result.append(i32 & 0xff)
    i32 = rshift(i32, 8)
    result.append(i32 & 0xff)
    return result

def get_elem(elem, tag):
    return elem.getElementsByTagName(tag)

def get_attr(elem, attr):
    return elem.getAttribute(attr)

def get_text(elem):
    return elem.firstChild.nodeValue

def shift_time(time_str):
    ts = time_str[:-4]
    return time.mktime(time.strptime(ts)) - 60

def parse_pptv_xml(dom):
    channel = get_elem(dom, 'channel')[0]
    title = get_attr(channel, 'nm')
    file_list = get_elem(channel, 'file')[0]
    item_list = get_elem(file_list, 'item')
    streams_cnt = len(item_list)
    item_mlist = []
    for item in item_list:
        rid = get_attr(item, 'rid')
        file_type = get_attr(item, 'ft')
        size = get_attr(item, 'filesize')
        width = get_attr(item, 'width')
        height = get_attr(item, 'height')
        bitrate = get_attr(item, 'bitrate')
        res = '{}x{}@{}kbps'.format(width, height, bitrate)
        item_meta = (file_type, rid, size, res)
        item_mlist.append(item_meta)

    dt_list = get_elem(dom, 'dt')
    dragdata_list = get_elem(dom, 'dragdata')

    stream_mlist = []
    for dt in dt_list:
        file_type = get_attr(dt, 'ft')
        serv_time = get_text(get_elem(dt, 'st')[0])
        expr_time = get_text(get_elem(dt, 'key')[0])
        serv_addr = get_text(get_elem(dt, 'sh')[0])
        stream_meta = (file_type, serv_addr, expr_time, serv_time)
        stream_mlist.append(stream_meta)

    segs_mlist = []
    for dd in dragdata_list:
        file_type = get_attr(dd, 'ft')
        seg_list = get_elem(dd, 'sgm')
        segs = []
        segs_size = []
        for seg in seg_list:
            rid = get_attr(seg, 'rid')
            size = get_attr(seg, 'fs')
            segs.append(rid)
            segs_size.append(size)
        segs_meta = (file_type, segs, segs_size)
        segs_mlist.append(segs_meta)
    return title, item_mlist, stream_mlist, segs_mlist

#mergs 3 meta_data
def merge_meta(item_mlist, stream_mlist, segs_mlist):
    streams = {}
    for i in range(len(segs_mlist)):
        streams[str(i)] = {}

    for item in item_mlist:
        stream = streams[item[0]]
        stream['rid'] = item[1]
        stream['size'] = item[2]
        stream['res'] = item[3]

    for s in stream_mlist:
        stream = streams[s[0]]
        stream['serv_addr'] = s[1]
        stream['expr_time'] = s[2]
        stream['serv_time'] = s[3]

    for seg in segs_mlist:
        stream = streams[seg[0]]
        stream['segs'] = seg[1]
        stream['segs_size'] = seg[2]

    return streams


def make_url(stream):
    host = stream['serv_addr']
    rid = stream['rid']
    key = gen_key(shift_time(stream['serv_time']))
    key_expr = stream['expr_time']

    src = []
    for i, seg in enumerate(stream['segs']):
        url = 'http://{}/{}/{}?key={}&k={}'.format(host, i, rid, key, key_expr)
        url += '&fpp.ver=1.3.0.4&type='
        src.append(url)
    return src

class PPTV(VideoExtractor):
    name = 'PPTV'
    stream_types = [
            {'itag': '4'},
            {'itag': '3'},
            {'itag': '2'},
            {'itag': '1'},
            {'itag': '0'},
    ]

    def prepare(self, **kwargs):
        if self.url and not self.vid:
            if not re.match(r'http://v.pptv.com/show/(\w+)\.html', self.url):
                raise('Unknown url pattern')
            page_content = get_content(self.url,{"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"})
            self.vid = match1(page_content, r'webcfg\s*=\s*{"id":\s*(\d+)')

        if not self.vid:
            raise('Cannot find id')
        api_url = 'http://web-play.pptv.com/webplay3-0-{}.xml'.format(self.vid)
        api_url += '?appplt=flp&appid=pptv.flashplayer.vod&appver=3.4.2.28&type=&version=4'
        dom = parseString(get_content(api_url,{"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"}))
        self.title, m_items, m_streams, m_segs = parse_pptv_xml(dom)
        xml_streams = merge_meta(m_items, m_streams, m_segs)
        for stream_id in xml_streams:
            stream_data = xml_streams[stream_id]
            src = make_url(stream_data)
            self.streams[stream_id] = {
                    'container': 'mp4',
                    'video_profile': stream_data['res'],
                    'size': int(stream_data['size']),
                    'src': src
            }

'''
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
    assert re.match(r'http://v.pptv.com/show/(\w+)\.html', url)
    html = get_html(url)
    id = r1(r'webcfg\s*=\s*{"id":\s*(\d+)', html)
    assert id
    pptv_download_by_id(id, output_dir = output_dir, merge = merge, info_only = info_only)
'''
site = PPTV()
#site_info = "PPTV.com"
#download = pptv_download
download = site.download_by_url
download_playlist = playlist_not_supported('pptv')
