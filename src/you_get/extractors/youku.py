#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..common import *
from ..extractor import VideoExtractor

import base64
import time
import traceback
import urllib.parse
import math
import pdb

class Youku(VideoExtractor):
    name = "优酷 (Youku)"

    # Last updated: 2015-11-24
    stream_types = [
        {'id': 'mp4hd3', 'alias-of' : 'hd3'},
        {'id': 'hd3',    'container': 'flv', 'video_profile': '1080P'},
        {'id': 'mp4hd2', 'alias-of' : 'hd2'},
        {'id': 'hd2',    'container': 'flv', 'video_profile': '超清'},
        {'id': 'mp4hd',  'alias-of' : 'mp4'},
        {'id': 'mp4',    'container': 'mp4', 'video_profile': '高清'},
        {'id': 'flvhd',  'container': 'flv', 'video_profile': '标清'},
        {'id': 'flv',    'container': 'flv', 'video_profile': '标清'},
        {'id': '3gphd',  'container': 'mp4', 'video_profile': '标清（3GP）'},
    ]


    def trans_e(a, c):
        f = h = 0
        b = list(range(256))
        result = ''
        while h < 256:
            f = (f + b[h] + ord(a[h % len(a)])) % 256
            b[h], b[f] = b[f], b[h]
            h += 1
        q = f = h = 0
        while q < len(c):
            h = (h + 1) % 256
            f = (f + b[h]) % 256
            b[h], b[f] = b[f], b[h]
            if isinstance(c[q], int):
                result += chr(c[q] ^ b[(b[h] + b[f]) % 256])
            else:
                result += chr(ord(c[q]) ^ b[(b[h] + b[f]) % 256])
            q += 1

        return result

    def generate_ep(no,streamfileids,sid,token):
        f_code_2 = 'bf7e5f01'

        def trans_e(a, c):
            f = h = 0
            b = list(range(256))
            result = ''
            while h < 256:
                f = (f + b[h] + ord(a[h % len(a)])) % 256
                b[h], b[f] = b[f], b[h]
                h += 1
            q = f = h = 0
            while q < len(c):
                h = (h + 1) % 256
                f = (f + b[h]) % 256
                b[h], b[f] = b[f], b[h]
                if isinstance(c[q], int):
                    result += chr(c[q] ^ b[(b[h] + b[f]) % 256])
                else:
                    result += chr(ord(c[q]) ^ b[(b[h] + b[f]) % 256])
                q += 1

            return result


        number = hex(int(str(no),10))[2:].upper()
        if len(number) == 1:
            number = '0' + number
        fileId = streamfileids[0:8] + number + streamfileids[10:]

        ep = urllib.parse.quote(base64.b64encode(''.join(trans_e(f_code_2,sid+'_'+fileId+'_'+token)).encode('latin1')),safe='~()*!.\'')
        return fileId,ep
    def parse_m3u8(m3u8):
        return re.findall('(http://[^\r]+)\r',m3u8)
#        return re.findall(r'(http://[^?]+)\?ts_start=0', m3u8)

    def get_vid_from_url(url):
        """Extracts video ID from URL.
        """
        return match1(url, r'youku\.com/v_show/id_([a-zA-Z0-9=]+)') or \
          match1(url, r'player\.youku\.com/player\.php/sid/([a-zA-Z0-9=]+)/v\.swf') or \
          match1(url, r'loader\.swf\?VideoIDS=([a-zA-Z0-9=]+)') or \
          match1(url, r'player\.youku\.com/embed/([a-zA-Z0-9=]+)')

    def get_playlist_id_from_url(url):
        """Extracts playlist ID from URL.
        """
        return match1(url, r'youku\.com/playlist_show/id_([a-zA-Z0-9=]+)')

    def download_playlist_by_url(self, url, **kwargs):
        self.url = url

        try:
            playlist_id = self.__class__.get_playlist_id_from_url(self.url)
            assert playlist_id

            video_page = get_content('http://www.youku.com/playlist_show/id_%s' % playlist_id)
            videos = set(re.findall(r'href="(http://v\.youku\.com/[^?"]+)', video_page))

            for extra_page_url in set(re.findall('href="(http://www\.youku\.com/playlist_show/id_%s_[^?"]+)' % playlist_id, video_page)):
                extra_page = get_content(extra_page_url)
                videos |= set(re.findall(r'href="(http://v\.youku\.com/[^?"]+)', extra_page))

        except:
            video_page = get_content(url)
            videos = set(re.findall(r'href="(http://v\.youku\.com/[^?"]+)', video_page))

        self.title = r1(r'<meta name="title" content="([^"]+)"', video_page) or \
                     r1(r'<title>([^<]+)', video_page)
        self.p_playlist()
        for video in videos:
            index = parse_query_param(video, 'f')
            try:
                self.__class__().download_by_url(video, index=index, **kwargs)
            except KeyboardInterrupt:
                raise
            except:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                traceback.print_exception(exc_type, exc_value, exc_traceback)

    def prepare(self, **kwargs):
        self.streams_parameter = {}
        assert self.url or self.vid

        if self.url and not self.vid:
            self.vid = self.__class__.get_vid_from_url(self.url)

            if self.vid is None:
                self.download_playlist_by_url(self.url, **kwargs)
                exit(0)

        api_url = 'http://play.youku.com/play/get.json?vid=%s&ct=12' % self.vid
        api_url1 = 'http://play.youku.com/play/get.json?vid=%s&ct=10' % self.vid
        try:
            meta = json.loads(get_html(api_url))
            meta1 = json.loads(get_html(api_url1))
            data = meta['data']
            data1 = meta1['data']
            assert 'stream' in data
        except:
            if 'error' in data:
                if data['error']['code'] == -202:
                    # Password protected
                    self.password_protected = True
                    self.password = input(log.sprint('Password: ', log.YELLOW))
                    api_url += '&pwd={}'.format(self.password)
                    api_url1 += '&pwd={}'.format(self.password)
                    meta1 = json.loads(get_html(api_url1))
                    meta = json.loads(get_html(api_url))
                    data1 = meta1['data']
                    data = meta['data']
                else:
                    log.wtf('[Failed] ' + data['error']['note'])
            else:
                log.wtf('[Failed] Video not found.')

        self.title = data['video']['title']
        self.ep = data['security']['encrypt_string']
        self.ip = data['security']['ip']

        stream_types = dict([(i['id'], i) for i in self.stream_types])

        for stream in data1['stream']:
            stream_id = stream['stream_type']
            if stream_id in stream_types:
                if 'alias-of' in stream_types[stream_id]:
                    stream_id = stream_types[stream_id]['alias-of']
                if stream_id not in self.streams_parameter:
                    self.streams_parameter[stream_id] = {
                            'fileid': stream['stream_fileid'],
                            'segs': stream['segs']
                            }

        for stream in data['stream']:
            stream_id = stream['stream_type']
            if stream_id in stream_types:
                if 'alias-of' in stream_types[stream_id]:
                    stream_id = stream_types[stream_id]['alias-of']
                self.streams[stream_id] = {
                    'container': stream_types[stream_id]['container'],
                    'video_profile': stream_types[stream_id]['video_profile'],
                    'size': stream['size']
                }
                if stream_id not in self.streams_parameter:
                    self.streams_parameter[stream_id] = {
                            'fileid': stream['stream_fileid'],
                            'segs': stream['segs']
                            }

        # Audio languages
        if 'dvd' in data and 'audiolang' in data['dvd']:
            self.audiolang = data['dvd']['audiolang']
            for i in self.audiolang:
                i['url'] = 'http://v.youku.com/v_show/id_{}'.format(i['vid'])

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

        f_code_1 = 'becaf9be'
        e_code = self.__class__.trans_e(f_code_1, base64.b64decode(bytes(self.ep, 'ascii')))

        sid, token = e_code.split('_')

        m3u8 = ''
        segs = self.streams_parameter[stream_id]['segs']
        streamfileid = self.streams_parameter[stream_id]['fileid']
        for no in range(0,len(segs)):
            k = segs[no]['key']
            if k == -1:
                log.e('Error')
                exit()
            fileId,ep  = self.__class__.generate_ep(no,streamfileid ,sid,token)
#            pdb.set_trace()
            m3u8  += 'http://k.youku.com/player/getFlvPath/sid/'+ sid
            m3u8+='_00/st/'+ self.streams[stream_id]['container']
            m3u8+='/fileid/'+ fileId
            m3u8+='?K='+ k
            m3u8+='&ctype=12&ev=1&token='+ token
            m3u8+='&oip='+ str(self.ip)
            m3u8+='&ep='+ ep+'\r\n'

        if not kwargs['info_only']:
            self.streams[stream_id]['src'] = self.__class__.parse_m3u8(m3u8)
            if not self.streams[stream_id]['src'] and self.password_protected:
                log.e('[Failed] Wrong password.')


#        if not kwargs['info_only']:
#            if self.password_protected:
#                m3u8_url += '&password={}'.format(self.password)
#
#            m3u8 = get_html(m3u8_url)
#
#            self.streams[stream_id]['src'] = self.__class__.parse_m3u8(m3u8)
#            if not self.streams[stream_id]['src'] and self.password_protected:
#                log.e('[Failed] Wrong password.')

site = Youku()
download = site.download_by_url
download_playlist = site.download_playlist_by_url

youku_download_by_vid = site.download_by_vid
# Used by: acfun.py bilibili.py miomio.py tudou.py
