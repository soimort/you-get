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
        url += '&type=web.fpp'
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
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/69.0.3497.100 Safari/537.36"
        }
        self.vid = match1(self.url, r'https?://sports.pptv.com/vod/(\d+)/*')
        if self.url and not self.vid:
            if not re.match(r'https?://v.pptv.com/show/(\w+)\.html', self.url):
                raise('Unknown url pattern')
            page_content = get_content(self.url, headers)

            self.vid = match1(page_content, r'webcfg\s*=\s*{"id":\s*(\d+)')
            if not self.vid:
                request = urllib.request.Request(self.url, headers=headers)
                response = urllib.request.urlopen(request)
                self.vid = match1(response.url, r'https?://sports.pptv.com/vod/(\d+)/*')

        if not self.vid:
            raise('Cannot find id')
        api_url = 'http://web-play.pptv.com/webplay3-0-{}.xml'.format(self.vid)
        api_url += '?type=web.fpp&param=type=web.fpp&version=4'
        dom = parseString(get_content(api_url, headers))
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

site = PPTV()
#site_info = "PPTV.com"
#download = pptv_download
download = site.download_by_url
download_playlist = playlist_not_supported('pptv')
