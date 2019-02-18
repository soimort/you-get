#!/usr/bin/env python

from ..common import *
from ..extractor import VideoExtractor

import hashlib

class Bilibili(VideoExtractor):
    name = "Bilibili"

    # Bilibili media encoding options, in descending quality order.
    stream_types = [
        {'id': 'flv_p60', 'quality': 116, 'audio_quality': 30280,
         'container': 'FLV', 'video_resolution': '1080p', 'desc': '高清 1080P60'},
        # 'id': 'hdflv2', 'quality': 112?
        {'id': 'flv', 'quality': 80, 'audio_quality': 30280,
         'container': 'FLV', 'video_resolution': '1080p', 'desc': '高清 1080P'},
        {'id': 'flv720_p60', 'quality': 74, 'audio_quality': 30280,
         'container': 'FLV', 'video_resolution': '720p', 'desc': '高清 720P60'},
        {'id': 'flv720', 'quality': 64, 'audio_quality': 30280,
         'container': 'FLV', 'video_resolution': '720p', 'desc': '高清 720P'},
        {'id': 'hdmp4', 'quality': 48, 'audio_quality': 30280,
         'container': 'MP4', 'video_resolution': '720p', 'desc': '高清 720P (MP4)'},
        {'id': 'flv480', 'quality': 32, 'audio_quality': 30280,
         'container': 'FLV', 'video_resolution': '480p', 'desc': '清晰 480P'},
        {'id': 'flv360', 'quality': 16, 'audio_quality': 30216,
         'container': 'FLV', 'video_resolution': '360p', 'desc': '流畅 360P'},
        # 'quality': 15?
    ]

    @staticmethod
    def bilibili_headers(referer=None, cookie=None):
        # a reasonable UA
        ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
        headers = {'User-Agent': ua}
        if referer is not None:
            headers.update({'Referer': referer})
        if cookie is not None:
            headers.update({'Cookie': cookie})
        return headers

    @staticmethod
    def bilibili_api(avid, cid, qn=0):
        return 'https://api.bilibili.com/x/player/playurl?avid=%s&cid=%s&qn=%s&type=&otype=json&fnver=0&fnval=16' % (avid, cid, qn)

    @staticmethod
    def bilibili_bangumi_api(avid, cid, ep_id, qn=0):
        return 'https://api.bilibili.com/pgc/player/web/playurl?avid=%s&cid=%s&qn=%s&type=&otype=json&ep_id=%s&fnver=0&fnval=16' % (avid, cid, qn, ep_id)

    @staticmethod
    def bilibili_interface_api(cid, qn=0):
        entropy = 'rbMCKn@KuamXWlPMoJGsKcbiJKUfkPF_8dABscJntvqhRSETg'
        appkey, sec = ''.join([chr(ord(i) + 2) for i in entropy[::-1]]).split(':')
        params = 'appkey=%s&cid=%s&otype=json&qn=%s&quality=%s&type=' % (appkey, cid, qn, qn)
        chksum = hashlib.md5(bytes(params + sec, 'utf8')).hexdigest()
        return 'http://interface.bilibili.com/v2/playurl?%s&sign=%s' % (params, chksum)

    def prepare(self, **kwargs):
        self.stream_qualities = {s['quality']: s for s in self.stream_types}

        html_content = get_content(self.url, headers=self.bilibili_headers())
        #self.title = match1(html_content,
        #                    r'<h1 title="([^"]+)"')

        # redirect: bangumi/play/ss -> bangumi/play/ep
        if re.match(r'https?://(www)?\.bilibili\.com/bangumi/play/ss(\d+)', self.url):
            initial_state_text = match1(html_content, r'__INITIAL_STATE__=(.*?);\(function\(\)')  # FIXME
            initial_state = json.loads(initial_state_text)
            ep_id = initial_state['epList'][0]['id']
            self.url = 'https://www.bilibili.com/bangumi/play/ep%s' % ep_id
            html_content = get_content(self.url, headers=self.bilibili_headers())

        # sort it out
        if re.match(r'https?://(www)?\.bilibili\.com/bangumi/play/ep(\d+)', self.url):
            sort = 'bangumi'
        elif match1(html_content, r'<meta property="og:url" content="(https://www.bilibili.com/bangumi/play/[^"]+)"'):
            sort = 'bangumi'
        elif re.match(r'https?://(www)?\.bilibili\.com/video/av(\d+)', self.url):
            sort = 'video'

        # regular av video
        if sort == 'video':
            initial_state_text = match1(html_content, r'__INITIAL_STATE__=(.*?);\(function\(\)')  # FIXME
            initial_state = json.loads(initial_state_text)

            playinfo_text = match1(html_content, r'__playinfo__=(.*?)</script><script>')  # FIXME
            playinfo = json.loads(playinfo_text) if playinfo_text else None

            html_content_ = get_content(self.url, headers=self.bilibili_headers(cookie='CURRENT_FNVAL=16'))
            playinfo_text_ = match1(html_content_, r'__playinfo__=(.*?)</script><script>')  # FIXME
            playinfo_ = json.loads(playinfo_text_) if playinfo_text_ else None

            # warn if it is a multi-part video
            pn = initial_state['videoData']['videos']
            if pn > 1 and not kwargs.get('playlist'):
                log.w('This is a multipart video. (use --playlist to download all parts.)')

            # set video title
            self.title = initial_state['videoData']['title']
            # refine title for a specific part, if it is a multi-part video
            p = int(match1(self.url, r'[\?&]p=(\d+)') or match1(self.url, r'/index_(\d+)') or
                    '1')  # use URL to decide p-number, not initial_state['p']
            if pn > 1:
                part = initial_state['videoData']['pages'][p - 1]['part']
                self.title = '%s (P%s. %s)' % (self.title, p, part)

            # construct playinfos
            avid = initial_state['aid']
            cid = initial_state['videoData']['pages'][p - 1]['cid']  # use p-number, not initial_state['videoData']['cid']
            current_quality, best_quality = None, None
            if playinfo is not None:
                current_quality = playinfo['data']['quality'] or None  # 0 indicates an error, fallback to None
                if 'accept_quality' in playinfo['data'] and playinfo['data']['accept_quality'] != []:
                    best_quality = playinfo['data']['accept_quality'][0]
            playinfos = []
            if playinfo is not None:
                playinfos.append(playinfo)
            if playinfo_ is not None:
                playinfos.append(playinfo_)
            # get alternative formats from API
            for qn in [80, 64, 32, 16]:
                # automatic format for durl: qn=0
                # for dash, qn does not matter
                if current_quality is None or qn < current_quality:
                    api_url = self.bilibili_api(avid, cid, qn=qn)
                    api_content = get_content(api_url, headers=self.bilibili_headers())
                    api_playinfo = json.loads(api_content)
                    if api_playinfo['code'] == 0:  # success
                        playinfos.append(api_playinfo)
                    else:
                        message = api_playinfo['data']['message']
                if best_quality is None or qn <= best_quality:
                    api_url = self.bilibili_interface_api(cid, qn=qn)
                    api_content = get_content(api_url, headers=self.bilibili_headers())
                    api_playinfo_data = json.loads(api_content)
                    if api_playinfo_data.get('quality'):
                        playinfos.append({'code': 0, 'message': '0', 'ttl': 1, 'data': api_playinfo_data})
            if not playinfos:
                log.w(message)
                # use bilibili error video instead
                url = 'https://static.hdslb.com/error.mp4'
                _, container, size = url_info(url)
                self.streams['flv480'] = {'container': container, 'size': size, 'src': [url]}
                return

            for playinfo in playinfos:
                quality = playinfo['data']['quality']
                format_id = self.stream_qualities[quality]['id']
                container = self.stream_qualities[quality]['container'].lower()
                desc = self.stream_qualities[quality]['desc']

                if 'durl' in playinfo['data']:
                    src, size = [], 0
                    for durl in playinfo['data']['durl']:
                        src.append(durl['url'])
                        size += durl['size']
                    self.streams[format_id] = {'container': container, 'quality': desc, 'size': size, 'src': src}

                # DASH formats
                if 'dash' in playinfo['data']:
                    for video in playinfo['data']['dash']['video']:
                        # prefer the latter codecs!
                        s = self.stream_qualities[video['id']]
                        format_id = 'dash-' + s['id']  # prefix
                        container = 'mp4'  # enforce MP4 container
                        desc = s['desc']
                        audio_quality = s['audio_quality']
                        baseurl = video['baseUrl']
                        size = url_size(baseurl, headers=self.bilibili_headers(referer=self.url))

                        # find matching audio track
                        audio_baseurl = playinfo['data']['dash']['audio'][0]['baseUrl']
                        for audio in playinfo['data']['dash']['audio']:
                            if int(audio['id']) == audio_quality:
                                audio_baseurl = audio['baseUrl']
                                break
                        size += url_size(audio_baseurl, headers=self.bilibili_headers(referer=self.url))

                        self.dash_streams[format_id] = {'container': container, 'quality': desc,
                                                        'src': [[baseurl], [audio_baseurl]], 'size': size}

        # bangumi
        elif sort == 'bangumi':
            initial_state_text = match1(html_content, r'__INITIAL_STATE__=(.*?);\(function\(\)')  # FIXME
            initial_state = json.loads(initial_state_text)

            # set video title
            self.title = initial_state['h1Title']

            # warn if this bangumi has more than 1 video
            epn = len(initial_state['epList'])
            if epn > 1 and not kwargs.get('playlist'):
                log.w('This bangumi currently has %s videos. (use --playlist to download all videos.)' % epn)

            ep_id = initial_state['epInfo']['id']
            avid = initial_state['epInfo']['aid']
            cid = initial_state['epInfo']['cid']
            api_url = self.bilibili_bangumi_api(avid, cid, ep_id)
            api_content = get_content(api_url, headers=self.bilibili_headers())
            data = json.loads(api_content)
            if data['code'] < 0:  # error
                log.e(data['message'])
                return

            # DASH formats
            for video in data['result']['dash']['video']:
                # convert height to quality code
                if video['height'] == 360:
                    quality = 16
                elif video['height'] == 480:
                    quality = 32
                elif video['height'] == 720:
                    quality = 64
                elif video['height'] == 1080:
                    quality = 80
                s = self.stream_qualities[quality]
                format_id = 'dash-' + s['id']  # prefix
                container = 'mp4'  # enforce MP4 container
                desc = s['desc']
                audio_quality = s['audio_quality']
                baseurl = video['baseUrl']
                size = url_size(baseurl, headers=self.bilibili_headers(referer=self.url))

                # find matching audio track
                audio_baseurl = data['result']['dash']['audio'][0]['baseUrl']
                for audio in data['result']['dash']['audio']:
                    if int(audio['id']) == audio_quality:
                        audio_baseurl = audio['baseUrl']
                        break
                size += url_size(audio_baseurl, headers=self.bilibili_headers(referer=self.url))

                self.dash_streams[format_id] = {'container': container, 'quality': desc,
                                                'src': [[baseurl], [audio_baseurl]], 'size': size}


        else:
            # NOT IMPLEMENTED
            pass

    def extract(self, **kwargs):
        # set UA and referer for downloading
        headers = self.bilibili_headers(referer=self.url)
        self.ua, self.referer = headers['User-Agent'], headers['Referer']

        if not self.streams_sorted:
            # no stream is available
            return

        if 'stream_id' in kwargs and kwargs['stream_id']:
            # extract the stream
            stream_id = kwargs['stream_id']
            if stream_id not in self.streams and stream_id not in self.dash_streams:
                log.e('[Error] Invalid video format.')
                log.e('Run \'-i\' command with no specific video format to view all available formats.')
                exit(2)
        else:
            # extract stream with the best quality
            stream_id = self.streams_sorted[0]['id']

    def download_playlist_by_url(self, url, **kwargs):
        self.url = url
        kwargs['playlist'] = True

        html_content = get_content(self.url, headers=self.bilibili_headers())

        # sort it out
        if re.match(r'https?://(www)?\.bilibili\.com/bangumi/play/ep(\d+)', self.url):
            sort = 'bangumi'
        elif match1(html_content, r'<meta property="og:url" content="(https://www.bilibili.com/bangumi/play/[^"]+)"'):
            sort = 'bangumi'
        elif re.match(r'https?://(www)?\.bilibili\.com/video/av(\d+)', self.url):
            sort = 'video'

        # regular av video
        if sort == 'video':
            initial_state_text = match1(html_content, r'__INITIAL_STATE__=(.*?);\(function\(\)')  # FIXME
            initial_state = json.loads(initial_state_text)
            aid = initial_state['videoData']['aid']
            pn = initial_state['videoData']['videos']
            for pi in range(1, pn + 1):
                purl = 'https://www.bilibili.com/video/av%s?p=%s' % (aid, pi)
                self.__class__().download_by_url(purl, **kwargs)

        elif sort == 'bangumi':
            initial_state_text = match1(html_content, r'__INITIAL_STATE__=(.*?);\(function\(\)')  # FIXME
            initial_state = json.loads(initial_state_text)
            for ep in initial_state['epList']:
                ep_id = ep['id']
                epurl = 'https://www.bilibili.com/bangumi/play/ep%s/' % ep_id
                self.__class__().download_by_url(epurl, **kwargs)


site = Bilibili()
download = site.download_by_url
download_playlist = site.download_playlist_by_url

bilibili_download = download
