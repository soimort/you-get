#!/usr/bin/env python

import json
import urllib.parse
import base64
import binascii
import re

from ..extractors import VideoExtractor
from ..util import log
from ..common import get_content, playlist_not_supported

__all__ = ['funshion_download']


class KBaseMapping:
    def __init__(self, base=62):
        self.base = base
        mapping_table = [str(num) for num in range(10)]
        for i in range(26):
            mapping_table.append(chr(i + ord('a')))
        for i in range(26):
            mapping_table.append(chr(i + ord('A')))

        self.mapping_table = mapping_table[:self.base]

    def mapping(self, num):
        res = []
        while num > 0:
            res.append(self.mapping_table[num % self.base])
            num = num // self.base
        return ''.join(res[::-1])


class Funshion(VideoExtractor):
    name = "funshion"
    stream_types = [
        {'id': 'sdvd'},
        {'id': 'sdvd_h265'},
        {'id': 'hd'},
        {'id': 'hd_h265'},
        {'id': 'dvd'},
        {'id': 'dvd_h265'},
        {'id': 'tv'},
        {'id': 'tv_h265'}
    ]
    a_mobile_url = 'http://m.fun.tv/implay/?mid=302555'
    video_ep = 'http://pv.funshion.com/v7/video/play/?id={}&cl=mweb&uc=111'
    media_ep = 'http://pm.funshion.com/v7/media/play/?id={}&cl=mweb&uc=111'
    coeff = None

    @classmethod
    def fetch_magic(cls, url):
        def search_dict(a_dict, target):
            for key, val in a_dict.items():
                if val == target:
                    return key

        magic_list = []

        page = get_content(url)
        src = re.findall(r'src="(.+?)"', page)
        js = [path for path in src if path.endswith('.js')]

        host = 'http://' + urllib.parse.urlparse(url).netloc
        js_path = [urllib.parse.urljoin(host, rel_path) for rel_path in js]

        for p in js_path:
            if 'mtool' in p or 'mcore' in p:
                js_text = get_content(p)
                hit = re.search(r'\(\'(.+?)\',(\d+),(\d+),\'(.+?)\'\.split\(\'\|\'\),\d+,\{\}\)', js_text)

                code = hit.group(1)
                base = hit.group(2)
                size = hit.group(3)
                names = hit.group(4).split('|')

                mapping = KBaseMapping(base=int(base))
                sym_to_name = {}
                for no in range(int(size), 0, -1):
                    no_in_base = mapping.mapping(no)
                    val = names[no] if no < len(names) and names[no] else no_in_base
                    sym_to_name[no_in_base] = val

                moz_ec_name = search_dict(sym_to_name, 'mozEcName')
                push = search_dict(sym_to_name, 'push')
                patt = '{}\.{}\("(.+?)"\)'.format(moz_ec_name, push)
                ec_list = re.findall(patt, code)
                [magic_list.append(sym_to_name[ec]) for ec in ec_list]
        return magic_list

    @classmethod
    def get_coeff(cls, magic_list):
        magic_set = set(magic_list)
        no_dup = []
        for item in magic_list:
            if item in magic_set:
                magic_set.remove(item)
                no_dup.append(item)
        # really necessary?

        coeff = [0, 0, 0, 0]
        for num_pair in no_dup:
            idx = int(num_pair[-1])
            val = int(num_pair[:-1], 16)
            coeff[idx] = val

        return coeff

    @classmethod
    def funshion_decrypt(cls, a_bytes, coeff):
        res_list = []
        pos = 0
        while pos < len(a_bytes):
            a = a_bytes[pos]
            if pos == len(a_bytes) - 1:
                res_list.append(a)
                pos += 1
            else:
                b = a_bytes[pos + 1]
                m = a * coeff[0] + b * coeff[2]
                n = a * coeff[1] + b * coeff[3]
                res_list.append(m & 0xff)
                res_list.append(n & 0xff)
                pos += 2
        return bytes(res_list).decode('utf8')

    @classmethod
    def funshion_decrypt_str(cls, a_str, coeff):
        # r'.{27}0' pattern, untested
        if len(a_str) == 28 and a_str[-1] == '0':
            data_bytes = base64.b64decode(a_str[:27] + '=')
            clear = cls.funshion_decrypt(data_bytes, coeff)
            return binascii.hexlify(clear.encode('utf8')).upper()

        data_bytes = base64.b64decode(a_str[2:])
        return cls.funshion_decrypt(data_bytes, coeff)

    @classmethod
    def checksum(cls, sha1_str):
        if len(sha1_str) != 41:
            return False
        if not re.match(r'[0-9A-Za-z]{41}', sha1_str):
            return False
        sha1 = sha1_str[:-1]
        if (15 & sum([int(char, 16) for char in sha1])) == int(sha1_str[-1], 16):
            return True
        return False

    @classmethod
    def get_cdninfo(cls, hashid):
        url = 'http://jobsfe.funshion.com/query/v1/mp4/{}.json'.format(hashid)
        meta = json.loads(get_content(url, decoded=False).decode('utf8'))
        return meta['playlist'][0]['urls']

    @classmethod
    def dec_playinfo(cls, info, coeff):
        res = None
        clear = cls.funshion_decrypt_str(info['infohash'], coeff)
        if cls.checksum(clear):
            res = dict(hashid=clear[:40], token=cls.funshion_decrypt_str(info['token'], coeff))
        else:
            clear = cls.funshion_decrypt_str(info['infohash_prev'], coeff)
            if cls.checksum(clear):
                res = dict(hashid=clear[:40], token=cls.funshion_decrypt_str(info['token_prev'], coeff))
        return res

    def prepare(self, **kwargs):
        if self.__class__.coeff is None:
            magic_list = self.__class__.fetch_magic(self.__class__.a_mobile_url)
            self.__class__.coeff = self.__class__.get_coeff(magic_list)

        if 'title' not in kwargs:
            url = 'http://pv.funshion.com/v5/video/profile/?id={}&cl=mweb&uc=111'.format(self.vid)
            meta = json.loads(get_content(url))
            self.title = meta['name']
        else:
            self.title = kwargs['title']

        ep_url = self.__class__.video_ep if 'single_video' in kwargs else self.__class__.media_ep

        url = ep_url.format(self.vid)
        meta = json.loads(get_content(url))
        streams = meta['playlist']
        for stream in streams:
            definition = stream['code']
            for s in stream['playinfo']:
                codec = 'h' + s['codec'][2:]
                # h.264 -> h264
                for st in self.__class__.stream_types:
                    s_id = '{}_{}'.format(definition, codec)
                    if codec == 'h264':
                        s_id = definition
                    if s_id == st['id']:
                        clear_info = self.__class__.dec_playinfo(s, self.__class__.coeff)
                        cdn_list = self.__class__.get_cdninfo(clear_info['hashid'])
                        base_url = cdn_list[0]
                        vf = urllib.parse.quote(s['vf'])
                        video_size = int(s['filesize'])
                        token = urllib.parse.quote(base64.b64encode(clear_info['token'].encode('utf8')))
                        video_url = '{}?token={}&vf={}'.format(base_url, token, vf)
                        self.streams[s_id] = dict(size=video_size, src=[video_url], container='mp4')


def funshion_download(url, **kwargs):
    if re.match(r'http://www.fun.tv/vplay/v-(\w+)', url):
        vid = re.search(r'http://www.fun.tv/vplay/v-(\w+)', url).group(1)
        Funshion().download_by_vid(vid, single_video=True, **kwargs)
    elif re.match(r'http://www.fun.tv/vplay/.*g-(\w+)', url):
        epid = re.search(r'http://www.fun.tv/vplay/.*g-(\w+)', url).group(1)
        url = 'http://pm.funshion.com/v5/media/episode?id={}&cl=mweb&uc=111'.format(epid)
        meta = json.loads(get_content(url))
        drama_name = meta['name']

        extractor = Funshion()
        for ep in meta['episodes']:
            title = '{}_{}_{}'.format(drama_name, ep['num'], ep['name'])
            extractor.download_by_vid(ep['id'], title=title, **kwargs)
    else:
        log.wtf('Unknown url pattern')

site_info = "funshion"
download = funshion_download
download_playlist = playlist_not_supported('funshion')
