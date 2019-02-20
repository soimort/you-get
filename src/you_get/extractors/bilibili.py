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
        {'id': 'mp4', 'quality': 0},
    ]

    @staticmethod
    def height_to_quality(height):
        if height <= 360:
            return 16
        elif height <= 480:
            return 32
        elif height <= 720:
            return 64
        else:
            return 80

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
    def bilibili_audio_api(sid):
        return 'https://www.bilibili.com/audio/music-service-c/web/url?sid=%s' % sid

    @staticmethod
    def bilibili_audio_info_api(sid):
        return 'https://www.bilibili.com/audio/music-service-c/web/song/info?sid=%s' % sid

    @staticmethod
    def bilibili_audio_menu_info_api(sid):
        return 'https://www.bilibili.com/audio/music-service-c/web/menu/info?sid=%s' % sid

    @staticmethod
    def bilibili_audio_menu_song_api(sid, ps=100):
        return 'https://www.bilibili.com/audio/music-service-c/web/song/of-menu?sid=%s&pn=1&ps=%s' % (sid, ps)

    @staticmethod
    def bilibili_bangumi_api(avid, cid, ep_id, qn=0):
        return 'https://api.bilibili.com/pgc/player/web/playurl?avid=%s&cid=%s&qn=%s&type=&otype=json&ep_id=%s&fnver=0&fnval=16' % (avid, cid, qn, ep_id)

    @staticmethod
    def bilibili_interface_api(cid, qn=0):
        entropy = 'rbMCKn@KuamXWlPMoJGsKcbiJKUfkPF_8dABscJntvqhRSETg'
        appkey, sec = ''.join([chr(ord(i) + 2) for i in entropy[::-1]]).split(':')
        params = 'appkey=%s&cid=%s&otype=json&qn=%s&quality=%s&type=' % (appkey, cid, qn, qn)
        chksum = hashlib.md5(bytes(params + sec, 'utf8')).hexdigest()
        return 'https://interface.bilibili.com/v2/playurl?%s&sign=%s' % (params, chksum)

    @staticmethod
    def bilibili_live_api(cid):
        return 'https://api.live.bilibili.com/room/v1/Room/playUrl?cid=%s&quality=0&platform=web' % cid

    @staticmethod
    def bilibili_live_room_info_api(room_id):
        return 'https://api.live.bilibili.com/room/v1/Room/get_info?room_id=%s' % room_id

    @staticmethod
    def bilibili_live_room_init_api(room_id):
        return 'https://api.live.bilibili.com/room/v1/Room/room_init?id=%s' % room_id

    @staticmethod
    def bilibili_space_channel_api(mid, cid, ps=100):
        return 'https://api.bilibili.com/x/space/channel/video?mid=%s&cid=%s&pn=1&ps=%s&order=0&jsonp=jsonp' % (mid, cid, ps)

    @staticmethod
    def bilibili_space_favlist_api(vmid, fid, ps=100):
        return 'https://api.bilibili.com/x/space/fav/arc?vmid=%s&fid=%s&pn=1&ps=%s&order=0&jsonp=jsonp' % (vmid, fid, ps)

    @staticmethod
    def bilibili_space_video_api(mid, ps=100):
        return 'https://space.bilibili.com/ajax/member/getSubmitVideos?mid=%s&page=1&pagesize=%s&order=0&jsonp=jsonp' % (mid, ps)

    @staticmethod
    def bilibili_vc_api(video_id):
        return 'https://api.vc.bilibili.com/clip/v1/video/detail?video_id=%s' % video_id

    def prepare(self, **kwargs):
        self.stream_qualities = {s['quality']: s for s in self.stream_types}

        try:
            html_content = get_content(self.url, headers=self.bilibili_headers())
        except:
            html_content = ''  # live always returns 400 (why?)
        #self.title = match1(html_content,
        #                    r'<h1 title="([^"]+)"')

        # redirect: watchlater
        if re.match(r'https?://(www\.)?bilibili\.com/watchlater/#/av(\d+)', self.url):
            avid = match1(self.url, r'/av(\d+)')
            p = int(match1(self.url, r'/p(\d+)') or '1')
            self.url = 'https://www.bilibili.com/video/av%s?p=%s' % (avid, p)
            html_content = get_content(self.url, headers=self.bilibili_headers())

        # redirect: bangumi/play/ss -> bangumi/play/ep
        # redirect: bangumi.bilibili.com/anime -> bangumi/play/ep
        elif re.match(r'https?://(www\.)?bilibili\.com/bangumi/play/ss(\d+)', self.url) or \
             re.match(r'https?://bangumi\.bilibili\.com/anime/(\d+)/play', self.url):
            initial_state_text = match1(html_content, r'__INITIAL_STATE__=(.*?);\(function\(\)')  # FIXME
            initial_state = json.loads(initial_state_text)
            ep_id = initial_state['epList'][0]['id']
            self.url = 'https://www.bilibili.com/bangumi/play/ep%s' % ep_id
            html_content = get_content(self.url, headers=self.bilibili_headers())

        # sort it out
        if re.match(r'https?://(www\.)?bilibili\.com/audio/au(\d+)', self.url):
            sort = 'audio'
        elif re.match(r'https?://(www\.)?bilibili\.com/bangumi/play/ep(\d+)', self.url):
            sort = 'bangumi'
        elif match1(html_content, r'<meta property="og:url" content="(https://www.bilibili.com/bangumi/play/[^"]+)"'):
            sort = 'bangumi'
        elif re.match(r'https?://live\.bilibili\.com/', self.url):
            sort = 'live'
        elif re.match(r'https?://vc\.bilibili\.com/video/(\d+)', self.url):
            sort = 'vc'
        elif re.match(r'https?://(www\.)?bilibili\.com/video/av(\d+)', self.url):
            sort = 'video'
        else:
            self.download_playlist_by_url(self.url, **kwargs)
            return

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

            # get danmaku
            self.danmaku = get_content('http://comment.bilibili.com/%s.xml' % cid)

        # bangumi
        elif sort == 'bangumi':
            initial_state_text = match1(html_content, r'__INITIAL_STATE__=(.*?);\(function\(\)')  # FIXME
            initial_state = json.loads(initial_state_text)

            # warn if this bangumi has more than 1 video
            epn = len(initial_state['epList'])
            if epn > 1 and not kwargs.get('playlist'):
                log.w('This bangumi currently has %s videos. (use --playlist to download all videos.)' % epn)

            # set video title
            self.title = initial_state['h1Title']

            # construct playinfos
            ep_id = initial_state['epInfo']['id']
            avid = initial_state['epInfo']['aid']
            cid = initial_state['epInfo']['cid']
            playinfos = []
            api_url = self.bilibili_bangumi_api(avid, cid, ep_id)
            api_content = get_content(api_url, headers=self.bilibili_headers())
            api_playinfo = json.loads(api_content)
            if api_playinfo['code'] == 0:  # success
                playinfos.append(api_playinfo)
            else:
                log.e(api_playinfo['message'])
                return
            current_quality = api_playinfo['result']['quality']
            # get alternative formats from API
            for qn in [80, 64, 32, 16]:
                # automatic format for durl: qn=0
                # for dash, qn does not matter
                if qn != current_quality:
                    api_url = self.bilibili_bangumi_api(avid, cid, ep_id, qn=qn)
                    api_content = get_content(api_url, headers=self.bilibili_headers())
                    api_playinfo = json.loads(api_content)
                    if api_playinfo['code'] == 0:  # success
                        playinfos.append(api_playinfo)

            for playinfo in playinfos:
                if 'durl' in playinfo['result']:
                    quality = playinfo['result']['quality']
                    format_id = self.stream_qualities[quality]['id']
                    container = self.stream_qualities[quality]['container'].lower()
                    desc = self.stream_qualities[quality]['desc']

                    src, size = [], 0
                    for durl in playinfo['result']['durl']:
                        src.append(durl['url'])
                        size += durl['size']
                    self.streams[format_id] = {'container': container, 'quality': desc, 'size': size, 'src': src}

                # DASH formats
                if 'dash' in playinfo['result']:
                    for video in playinfo['result']['dash']['video']:
                        # playinfo['result']['quality'] does not reflect the correct quality of DASH stream
                        quality = self.height_to_quality(video['height'])  # convert height to quality code
                        s = self.stream_qualities[quality]
                        format_id = 'dash-' + s['id']  # prefix
                        container = 'mp4'  # enforce MP4 container
                        desc = s['desc']
                        audio_quality = s['audio_quality']
                        baseurl = video['baseUrl']
                        size = url_size(baseurl, headers=self.bilibili_headers(referer=self.url))

                        # find matching audio track
                        audio_baseurl = playinfo['result']['dash']['audio'][0]['baseUrl']
                        for audio in playinfo['result']['dash']['audio']:
                            if int(audio['id']) == audio_quality:
                                audio_baseurl = audio['baseUrl']
                                break
                        size += url_size(audio_baseurl, headers=self.bilibili_headers(referer=self.url))

                        self.dash_streams[format_id] = {'container': container, 'quality': desc,
                                                        'src': [[baseurl], [audio_baseurl]], 'size': size}

        # vc video
        elif sort == 'vc':
            video_id = match1(self.url, r'https?://vc\.?bilibili\.com/video/(\d+)')
            api_url = self.bilibili_vc_api(video_id)
            api_content = get_content(api_url, headers=self.bilibili_headers())
            api_playinfo = json.loads(api_content)

            # set video title
            self.title = '%s (%s)' % (api_playinfo['data']['user']['name'], api_playinfo['data']['item']['id'])

            height = api_playinfo['data']['item']['height']
            quality = self.height_to_quality(height)  # convert height to quality code
            s = self.stream_qualities[quality]
            format_id = s['id']
            container = 'mp4'  # enforce MP4 container
            desc = s['desc']

            playurl = api_playinfo['data']['item']['video_playurl']
            size = int(api_playinfo['data']['item']['video_size'])

            self.streams[format_id] = {'container': container, 'quality': desc, 'size': size, 'src': [playurl]}

        # live
        elif sort == 'live':
            m = re.match(r'https?://live\.bilibili\.com/(\w+)', self.url)
            short_id = m.group(1)
            api_url = self.bilibili_live_room_init_api(short_id)
            api_content = get_content(api_url, headers=self.bilibili_headers())
            room_init_info = json.loads(api_content)

            room_id = room_init_info['data']['room_id']
            api_url = self.bilibili_live_room_info_api(room_id)
            api_content = get_content(api_url, headers=self.bilibili_headers())
            room_info = json.loads(api_content)

            # set video title
            self.title = room_info['data']['title'] + '.' + str(int(time.time()))

            api_url = self.bilibili_live_api(room_id)
            api_content = get_content(api_url, headers=self.bilibili_headers())
            video_info = json.loads(api_content)

            durls = video_info['data']['durl']
            playurl = durls[0]['url']
            container = 'flv'  # enforce FLV container
            self.streams['flv'] = {'container': container, 'quality': 'unknown',
                                   'size': 0, 'src': [playurl]}

        # audio
        elif sort == 'audio':
            m = re.match(r'https?://(?:www\.)?bilibili\.com/audio/au(\d+)', self.url)
            sid = m.group(1)
            api_url = self.bilibili_audio_info_api(sid)
            api_content = get_content(api_url, headers=self.bilibili_headers())
            song_info = json.loads(api_content)

            # set audio title
            self.title = song_info['data']['title']

            lyric = song_info['data']['lyric']
            # TODO: download lyrics

            api_url = self.bilibili_audio_api(sid)
            api_content = get_content(api_url, headers=self.bilibili_headers())
            audio_info = json.loads(api_content)

            playurl = audio_info['data']['cdns'][0]
            size = audio_info['data']['size']
            container = 'mp4'  # enforce MP4 container
            self.streams['mp4'] = {'container': container,
                                   'size': size, 'src': [playurl]}

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
        if re.match(r'https?://(www\.)?bilibili\.com/bangumi/play/ep(\d+)', self.url):
            sort = 'bangumi'
        elif match1(html_content, r'<meta property="og:url" content="(https://www.bilibili.com/bangumi/play/[^"]+)"'):
            sort = 'bangumi'
        elif re.match(r'https?://(www\.)?bilibili\.com/bangumi/media/md(\d+)', self.url) or \
            re.match(r'https?://bangumi\.bilibili\.com/anime/(\d+)', self.url):
            sort = 'bangumi_md'
        elif re.match(r'https?://(www\.)?bilibili\.com/video/av(\d+)', self.url):
            sort = 'video'
        elif re.match(r'https?://space\.?bilibili\.com/(\d+)/channel/detail\?.*cid=(\d+)', self.url):
            sort = 'space_channel'
        elif re.match(r'https?://space\.?bilibili\.com/(\d+)/favlist\?.*fid=(\d+)', self.url):
            sort = 'space_favlist'
        elif re.match(r'https?://space\.?bilibili\.com/(\d+)/video', self.url):
            sort = 'space_video'
        elif re.match(r'https?://(www\.)?bilibili\.com/audio/am(\d+)', self.url):
            sort = 'audio_menu'
        else:
            log.e('[Error] Unsupported URL pattern.')
            exit(1)

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
            epn, i = len(initial_state['epList']), 0
            for ep in initial_state['epList']:
                i += 1; log.w('Extracting %s of %s videos ...' % (i, epn))
                ep_id = ep['id']
                epurl = 'https://www.bilibili.com/bangumi/play/ep%s/' % ep_id
                self.__class__().download_by_url(epurl, **kwargs)

        elif sort == 'bangumi_md':
            initial_state_text = match1(html_content, r'__INITIAL_STATE__=(.*?);\(function\(\)')  # FIXME
            initial_state = json.loads(initial_state_text)
            epn, i = len(initial_state['mediaInfo']['episodes']), 0
            for ep in initial_state['mediaInfo']['episodes']:
                i += 1; log.w('Extracting %s of %s videos ...' % (i, epn))
                ep_id = ep['ep_id']
                epurl = 'https://www.bilibili.com/bangumi/play/ep%s/' % ep_id
                self.__class__().download_by_url(epurl, **kwargs)

        elif sort == 'space_channel':
            m = re.match(r'https?://space\.?bilibili\.com/(\d+)/channel/detail\?.*cid=(\d+)', self.url)
            mid, cid = m.group(1), m.group(2)
            api_url = self.bilibili_space_channel_api(mid, cid)
            api_content = get_content(api_url, headers=self.bilibili_headers(referer=self.url))
            channel_info = json.loads(api_content)
            epn, i = len(channel_info['data']['list']['archives']), 0
            for video in channel_info['data']['list']['archives']:
                i += 1; log.w('Extracting %s of %s videos ...' % (i, epn))
                url = 'https://www.bilibili.com/video/av%s' % video['aid']
                self.__class__().download_playlist_by_url(url, **kwargs)

        elif sort == 'space_favlist':
            m = re.match(r'https?://space\.?bilibili\.com/(\d+)/favlist\?.*fid=(\d+)', self.url)
            vmid, fid = m.group(1), m.group(2)
            api_url = self.bilibili_space_favlist_api(vmid, fid)
            api_content = get_content(api_url, headers=self.bilibili_headers(referer=self.url))
            favlist_info = json.loads(api_content)
            epn, i = len(favlist_info['data']['archives']), 0
            for video in favlist_info['data']['archives']:
                i += 1; log.w('Extracting %s of %s videos ...' % (i, epn))
                url = 'https://www.bilibili.com/video/av%s' % video['aid']
                self.__class__().download_playlist_by_url(url, **kwargs)

        elif sort == 'space_video':
            m = re.match(r'https?://space\.?bilibili\.com/(\d+)/video', self.url)
            mid = m.group(1)
            api_url = self.bilibili_space_video_api(mid)
            api_content = get_content(api_url, headers=self.bilibili_headers())
            videos_info = json.loads(api_content)
            epn, i = len(videos_info['data']['vlist']), 0
            for video in videos_info['data']['vlist']:
                i += 1; log.w('Extracting %s of %s videos ...' % (i, epn))
                url = 'https://www.bilibili.com/video/av%s' % video['aid']
                self.__class__().download_playlist_by_url(url, **kwargs)

        elif sort == 'audio_menu':
            m = re.match(r'https?://(?:www\.)?bilibili\.com/audio/am(\d+)', self.url)
            sid = m.group(1)
            #api_url = self.bilibili_audio_menu_info_api(sid)
            #api_content = get_content(api_url, headers=self.bilibili_headers())
            #menu_info = json.loads(api_content)
            api_url = self.bilibili_audio_menu_song_api(sid)
            api_content = get_content(api_url, headers=self.bilibili_headers())
            menusong_info = json.loads(api_content)
            epn, i = len(menusong_info['data']['data']), 0
            for song in menusong_info['data']['data']:
                i += 1; log.w('Extracting %s of %s songs ...' % (i, epn))
                url = 'https://www.bilibili.com/audio/au%s' % song['id']
                self.__class__().download_by_url(url, **kwargs)


site = Bilibili()
download = site.download_by_url
download_playlist = site.download_playlist_by_url

bilibili_download = download
