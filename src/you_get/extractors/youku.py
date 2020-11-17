#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..common import *
from ..extractor import VideoExtractor

import time
import traceback
import json
import urllib.request
import urllib.parse


def fetch_cna():

    def quote_cna(val):
        if '%' in val:
            return val
        return urllib.parse.quote(val)

    if cookies:
        for cookie in cookies:
            if cookie.name == 'cna' and cookie.domain == '.youku.com':
                log.i('Found cna in imported cookies. Use it')
                return quote_cna(cookie.value)
    url = 'http://log.mmstat.com/eg.js'
    req = urllib.request.urlopen(url)
    headers = req.getheaders()
    for header in headers:
        if header[0].lower() == 'set-cookie':
            n_v = header[1].split(';')[0]
            name, value = n_v.split('=')
            if name == 'cna':
                return quote_cna(value)
    log.w('It seems that the client failed to fetch a cna cookie. Please load your own cookie if possible')
    return quote_cna('DOG4EdW4qzsCAbZyXbU+t7Jt')


class Youku(VideoExtractor):
    name = "优酷 (Youku)"
    mobile_ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36'
    dispatcher_url = 'vali.cp31.ott.cibntv.net'

    stream_types = [
        {'id': 'hd3',      'container': 'flv', 'video_profile': '1080P'},
        {'id': 'hd3v2',    'container': 'flv', 'video_profile': '1080P'},
        {'id': 'mp4hd3',   'container': 'mp4', 'video_profile': '1080P'},
        {'id': 'mp4hd3v2', 'container': 'mp4', 'video_profile': '1080P'},

        {'id': 'hd2',      'container': 'flv', 'video_profile': '超清'},
        {'id': 'hd2v2',    'container': 'flv', 'video_profile': '超清'},
        {'id': 'mp4hd2',   'container': 'mp4', 'video_profile': '超清'},
        {'id': 'mp4hd2v2', 'container': 'mp4', 'video_profile': '超清'},

        {'id': 'mp4hd',    'container': 'mp4', 'video_profile': '高清'},
        # not really equivalent to mp4hd
        {'id': 'flvhd',    'container': 'flv', 'video_profile': '渣清'},
        {'id': '3gphd',    'container': 'mp4', 'video_profile': '渣清'},

        {'id': 'mp4sd',    'container': 'mp4', 'video_profile': '标清'},
        # obsolete?
        {'id': 'flv',      'container': 'flv', 'video_profile': '标清'},
        {'id': 'mp4',      'container': 'mp4', 'video_profile': '标清'},
    ]

    def __init__(self):
        super().__init__()

        self.ua = self.__class__.mobile_ua
        self.referer = 'http://v.youku.com'

        self.page = None
        self.video_list = None
        self.video_next = None
        self.password = None
        self.api_data = None
        self.api_error_code = None
        self.api_error_msg = None

        self.ccode = '0590'
        # Found in http://g.alicdn.com/player/ykplayer/0.5.64/youku-player.min.js
        # grep -oE '"[0-9a-zA-Z+/=]{256}"' youku-player.min.js
        self.ckey = 'DIl58SLFxFNndSV1GFNnMQVYkx1PP5tKe1siZu/86PR1u/Wh1Ptd+WOZsHHWxysSfAOhNJpdVWsdVJNsfJ8Sxd8WKVvNfAS8aS8fAOzYARzPyPc3JvtnPHjTdKfESTdnuTW6ZPvk2pNDh4uFzotgdMEFkzQ5wZVXl2Pf1/Y6hLK0OnCNxBj3+nb0v72gZ6b0td+WOZsHHWxysSo/0y9D2K42SaB8Y/+aD2K42SaB8Y/+ahU+WOZsHcrxysooUeND'
        self.utid = None

    def youku_ups(self):
        url = 'https://ups.youku.com/ups/get.json?vid={}&ccode={}'.format(self.vid, self.ccode)
        url += '&client_ip=192.168.1.1'
        url += '&utid=' + self.utid
        url += '&client_ts=' + str(int(time.time()))
        url += '&ckey=' + urllib.parse.quote(self.ckey)
        if self.password_protected:
            url += '&password=' + self.password
        headers = dict(Referer=self.referer)
        headers['User-Agent'] = self.ua
        api_meta = json.loads(get_content(url, headers=headers))

        self.api_data = api_meta['data']
        data_error = self.api_data.get('error')
        if data_error:
            self.api_error_code = data_error.get('code')
            self.api_error_msg = data_error.get('note')
        if 'videos' in self.api_data:
            if 'list' in self.api_data['videos']:
                self.video_list = self.api_data['videos']['list']
            if 'next' in self.api_data['videos']:
                self.video_next = self.api_data['videos']['next']

    @classmethod
    def change_cdn(cls, url):
        # if the cnd_url starts with an ip addr, it should be youku's old CDN
        # which rejects http requests randomly with status code > 400
        # change it to the dispatcher of aliCDN can do better
        # at least a little more recoverable from HTTP 403
        if cls.dispatcher_url in url:
            return url
        elif 'k.youku.com' in url:
            return url
        else:
            url_seg_list = list(urllib.parse.urlsplit(url))
            url_seg_list[1] = cls.dispatcher_url
            return urllib.parse.urlunsplit(url_seg_list)

    def get_vid_from_url(self):
        # It's unreliable. check #1633
        b64p = r'([a-zA-Z0-9=]+)'
        p_list = [r'youku\.com/v_show/id_'+b64p,
                  r'player\.youku\.com/player\.php/sid/'+b64p+r'/v\.swf',
                  r'loader\.swf\?VideoIDS='+b64p,
                  r'player\.youku\.com/embed/'+b64p]
        if not self.url:
            raise Exception('No url')
        for p in p_list:
            hit = re.search(p, self.url)
            if hit is not None:
                self.vid = hit.group(1)
                return

    def get_vid_from_page(self):
        if not self.url:
            raise Exception('No url')
        self.page = get_content(self.url)
        hit = re.search(r'videoId2:"([A-Za-z0-9=]+)"', self.page)
        if hit is not None:
            self.vid = hit.group(1)

    def prepare(self, **kwargs):
        assert self.url or self.vid

        if self.url and not self.vid:
            self.get_vid_from_url()

            if self.vid is None:
                self.get_vid_from_page()

                if self.vid is None:
                    log.wtf('Cannot fetch vid')

        if kwargs.get('src') and kwargs['src'] == 'tudou':
            self.ccode = '0512'

        if kwargs.get('password') and kwargs['password']:
            self.password_protected = True
            self.password = kwargs['password']

        self.utid = fetch_cna()
        time.sleep(3)
        self.youku_ups()

        if self.api_data.get('stream') is None:
            if self.api_error_code == -6001:  # wrong vid parsed from the page
                vid_from_url = self.vid
                self.get_vid_from_page()
                if vid_from_url == self.vid:
                    log.wtf(self.api_error_msg)
                self.youku_ups()

        if self.api_data.get('stream') is None:
            if self.api_error_code == -2002:  # wrong password
                self.password_protected = True
                # it can be True already(from cli). offer another chance to retry
                self.password = input(log.sprint('Password: ', log.YELLOW))
                self.youku_ups()

        if self.api_data.get('stream') is None:
            if self.api_error_msg:
                log.wtf(self.api_error_msg)
            else:
                log.wtf('Unknown error')

        self.title = self.api_data['video']['title']
        stream_types = dict([(i['id'], i) for i in self.stream_types])
        audio_lang = self.api_data['stream'][0]['audio_lang']

        for stream in self.api_data['stream']:
            stream_id = stream['stream_type']
            is_preview = False
            if stream_id in stream_types and stream['audio_lang'] == audio_lang:
                if 'alias-of' in stream_types[stream_id]:
                    stream_id = stream_types[stream_id]['alias-of']

                if stream_id not in self.streams:
                    self.streams[stream_id] = {
                        'container': stream_types[stream_id]['container'],
                        'video_profile': stream_types[stream_id]['video_profile'],
                        'size': stream['size'],
                        'pieces': [{
                            'segs': stream['segs']
                        }],
                        'm3u8_url': stream['m3u8_url']
                    }
                    src = []
                    for seg in stream['segs']:
                        if seg.get('cdn_url'):
                            src.append(self.__class__.change_cdn(seg['cdn_url']))
                        else:
                            is_preview = True
                    self.streams[stream_id]['src'] = src
                else:
                    self.streams[stream_id]['size'] += stream['size']
                    self.streams[stream_id]['pieces'].append({
                        'segs': stream['segs']
                    })
                    src = []
                    for seg in stream['segs']:
                        if seg.get('cdn_url'):
                            src.append(self.__class__.change_cdn(seg['cdn_url']))
                        else:
                            is_preview = True
                    self.streams[stream_id]['src'].extend(src)
            if is_preview:
                log.w('{} is a preview'.format(stream_id))

        # Audio languages
        if 'dvd' in self.api_data:
            al = self.api_data['dvd'].get('audiolang')
            if al:
                self.audiolang = al
                for i in self.audiolang:
                    i['url'] = 'http://v.youku.com/v_show/id_{}'.format(i['vid'])


def youku_download_playlist_by_url(url, **kwargs):
    video_page_pt = 'https?://v.youku.com/v_show/id_([A-Za-z0-9=]+)'
    js_cb_pt = '\(({.+})\)'
    if re.match(video_page_pt, url):
        youku_obj = Youku()
        youku_obj.url = url
        youku_obj.prepare(**kwargs)
        total_episode = None
        try:
            total_episode = youku_obj.api_data['show']['episode_total']
        except KeyError:
            log.wtf('Cannot get total_episode for {}'.format(url))
        next_vid = youku_obj.vid
        for _ in range(total_episode):
            this_extractor = Youku()
            this_extractor.download_by_vid(next_vid, keep_obj=True, **kwargs)
            next_vid = this_extractor.video_next['encodevid']
        '''
        if youku_obj.video_list is None:
            log.wtf('Cannot find video list for {}'.format(url))
        else:
            vid_list = [v['encodevid'] for v in youku_obj.video_list]
            for v in vid_list:
                Youku().download_by_vid(v, **kwargs)
        '''

    elif re.match('https?://list.youku.com/show/id_', url):
        # http://list.youku.com/show/id_z2ae8ee1c837b11e18195.html
        # official playlist
        page = get_content(url)
        show_id = re.search(r'showid:"(\d+)"', page).group(1)
        ep = 'http://list.youku.com/show/module?id={}&tab=showInfo&callback=jQuery'.format(show_id)
        xhr_page = get_content(ep).replace('\/', '/').replace('\"', '"')
        video_url = re.search(r'(v.youku.com/v_show/id_(?:[A-Za-z0-9=]+)\.html)', xhr_page).group(1)
        youku_download_playlist_by_url('http://'+video_url, **kwargs)
        return
    elif re.match('https?://list.youku.com/albumlist/show/id_(\d+)\.html', url):
        # http://list.youku.com/albumlist/show/id_2336634.html
        # UGC playlist
        list_id = re.search('https?://list.youku.com/albumlist/show/id_(\d+)\.html', url).group(1)
        ep = 'http://list.youku.com/albumlist/items?id={}&page={}&size=20&ascending=1&callback=tuijsonp6'

        first_u = ep.format(list_id, 1)
        xhr_page = get_content(first_u)
        json_data = json.loads(re.search(js_cb_pt, xhr_page).group(1))
        video_cnt = json_data['data']['total']
        xhr_html = json_data['html']
        v_urls = re.findall(r'(v.youku.com/v_show/id_(?:[A-Za-z0-9=]+)\.html)', xhr_html)

        if video_cnt > 20:
            req_cnt = video_cnt // 20
            for i in range(2, req_cnt+2):
                req_u = ep.format(list_id, i)
                xhr_page = get_content(req_u)
                json_data = json.loads(re.search(js_cb_pt, xhr_page).group(1).replace('\/', '/'))
                xhr_html = json_data['html']
                page_videos = re.findall(r'(v.youku.com/v_show/id_(?:[A-Za-z0-9=]+)\.html)', xhr_html)
                v_urls.extend(page_videos)
        for u in v_urls[0::2]:
            url = 'http://' + u
            Youku().download_by_url(url, **kwargs)
        return


def youku_download_by_url(url, **kwargs):
    Youku().download_by_url(url, **kwargs)


def youku_download_by_vid(vid, **kwargs):
    Youku().download_by_vid(vid, **kwargs)

download = youku_download_by_url
download_playlist = youku_download_playlist_by_url
