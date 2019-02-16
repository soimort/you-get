#!/usr/bin/env python

from ..common import *
from ..extractor import VideoExtractor

class Bilibili(VideoExtractor):
    name = "Bilibili"

    # Bilibili media encoding options, in descending quality order.
    stream_types = [
        {'id': 'flv_p60', 'quality': 116, 'audio_quality': 30280,
         'container': 'MP4', 'video_resolution': '1080p', 'desc': '高清 1080P60'},
        {'id': 'flv', 'quality': 80, 'audio_quality': 30280,
         'container': 'MP4', 'video_resolution': '1080p', 'desc': '高清 1080P'},
        {'id': 'flv720_p60', 'quality': 74, 'audio_quality': 30280,
         'container': 'MP4', 'video_resolution': '720p', 'desc': '高清 720P60'},
        {'id': 'flv720', 'quality': 64, 'audio_quality': 30280,
         'container': 'MP4', 'video_resolution': '720p', 'desc': '高清 720P'},
        {'id': 'flv480', 'quality': 32, 'audio_quality': 30280,
         'container': 'MP4', 'video_resolution': '480p', 'desc': '清晰 480P'},  # default
        {'id': 'flv360', 'quality': 16, 'audio_quality': 30216,
         'container': 'MP4', 'video_resolution': '360p', 'desc': '流畅 360P'},
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

    def prepare(self, **kwargs):
        self.stream_qualities = {s['quality']: s for s in self.stream_types}

        html_content = get_content(self.url, headers=self.bilibili_headers())
        #self.title = match1(html_content,
        #                    r'<h1 title="([^"]+)"')

        # regular av
        # TODO: multi-P
        if re.match(r'https?://(www)?\.bilibili\.com/video/av(\d+)', self.url):
            playinfo_text = match1(html_content, r'__playinfo__=(.*?)</script><script>')  # FIXME
            playinfo = json.loads(playinfo_text)

            initial_state_text = match1(html_content, r'__INITIAL_STATE__=(.*?);\(function\(\)')  # FIXME
            initial_state = json.loads(initial_state_text)
            self.title = initial_state['videoData']['title']

            # determine default quality / format
            quality = int(playinfo['data']['quality'])
            format_id = self.stream_qualities[quality]['id']
            container = self.stream_qualities[quality]['container'].lower()
            desc = self.stream_qualities[quality]['desc']
            self.stream_types.append({'id': 'default'})

            # determine default source URL and size
            src, size = [], 0
            for durl in playinfo['data']['durl']:
                src.append(durl['url'])
                size += durl['size']
            self.streams['default'] = {'container': container, 'quality': desc, 'size': size, 'src': src}

            # DASH formats
            html_content_ = get_content(self.url, headers=self.bilibili_headers(cookie='CURRENT_FNVAL=16'))
            playinfo_text_ = match1(html_content_, r'__playinfo__=(.*?)</script><script>')  # FIXME
            playinfo_ = json.loads(playinfo_text_)
            for video in playinfo_['data']['dash']['video']:
                # prefer the latter codecs!
                s = self.stream_qualities[video['id']]
                format_id = s['id']
                container = s['container'].lower()
                desc = s['desc']
                audio_quality = s['audio_quality']
                baseurl = video['baseUrl']
                size = url_size(baseurl, headers=self.bilibili_headers(referer=self.url))

                # find matching audio track
                audio_baseurl = playinfo_['data']['dash']['audio'][0]['baseUrl']
                for audio in playinfo_['data']['dash']['audio']:
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


site = Bilibili()
download = site.download_by_url
# TODO: download_playlist

bilibili_download = download
