#!/usr/bin/env python

from ..common import *
from ..extractor import VideoExtractor

from xml.dom.minidom import parseString

class YouTube(VideoExtractor):
    name = "YouTube"

    # Non-DASH YouTube media encoding options, in descending quality order.
    # http://en.wikipedia.org/wiki/YouTube#Quality_and_codecs. Retrieved July 17, 2014.
    stream_types = [
        {'itag': '38', 'container': 'MP4', 'video_resolution': '3072p',
         'video_encoding': 'H.264', 'video_profile': 'High', 'video_bitrate': '3.5-5',
         'audio_encoding': 'AAC', 'audio_bitrate': '192'},
        #{'itag': '85', 'container': 'MP4', 'video_resolution': '1080p', 'video_encoding': 'H.264', 'video_profile': '3D', 'video_bitrate': '3-4', 'audio_encoding': 'AAC', 'audio_bitrate': '192'},
        {'itag': '46', 'container': 'WebM', 'video_resolution': '1080p',
         'video_encoding': 'VP8', 'video_profile': '', 'video_bitrate': '',
         'audio_encoding': 'Vorbis', 'audio_bitrate': '192'},
        {'itag': '37', 'container': 'MP4', 'video_resolution': '1080p',
         'video_encoding': 'H.264', 'video_profile': 'High', 'video_bitrate': '3-4.3',
         'audio_encoding': 'AAC', 'audio_bitrate': '192'},
        #{'itag': '102', 'container': 'WebM', 'video_resolution': '720p', 'video_encoding': 'VP8', 'video_profile': '3D', 'video_bitrate': '', 'audio_encoding': 'Vorbis', 'audio_bitrate': '192'},
        {'itag': '45', 'container': 'WebM', 'video_resolution': '720p',
         'video_encoding': 'VP8', 'video_profile': '', 'video_bitrate': '2',
         'audio_encoding': 'Vorbis', 'audio_bitrate': '192'},
        #{'itag': '84', 'container': 'MP4', 'video_resolution': '720p', 'video_encoding': 'H.264', 'video_profile': '3D', 'video_bitrate': '2-3', 'audio_encoding': 'AAC', 'audio_bitrate': '192'},
        {'itag': '22', 'container': 'MP4', 'video_resolution': '720p',
         'video_encoding': 'H.264', 'video_profile': 'High', 'video_bitrate': '2-3',
         'audio_encoding': 'AAC', 'audio_bitrate': '192'},
        {'itag': '120', 'container': 'FLV', 'video_resolution': '720p',
         'video_encoding': 'H.264', 'video_profile': 'Main@L3.1', 'video_bitrate': '2',
         'audio_encoding': 'AAC', 'audio_bitrate': '128'}, # Live streaming only
        {'itag': '44', 'container': 'WebM', 'video_resolution': '480p',
         'video_encoding': 'VP8', 'video_profile': '', 'video_bitrate': '1',
         'audio_encoding': 'Vorbis', 'audio_bitrate': '128'},
        {'itag': '35', 'container': 'FLV', 'video_resolution': '480p',
         'video_encoding': 'H.264', 'video_profile': 'Main', 'video_bitrate': '0.8-1',
         'audio_encoding': 'AAC', 'audio_bitrate': '128'},
        #{'itag': '101', 'container': 'WebM', 'video_resolution': '360p', 'video_encoding': 'VP8', 'video_profile': '3D', 'video_bitrate': '', 'audio_encoding': 'Vorbis', 'audio_bitrate': '192'},
        #{'itag': '100', 'container': 'WebM', 'video_resolution': '360p', 'video_encoding': 'VP8', 'video_profile': '3D', 'video_bitrate': '', 'audio_encoding': 'Vorbis', 'audio_bitrate': '128'},
        {'itag': '43', 'container': 'WebM', 'video_resolution': '360p',
         'video_encoding': 'VP8', 'video_profile': '', 'video_bitrate': '0.5',
         'audio_encoding': 'Vorbis', 'audio_bitrate': '128'},
        {'itag': '34', 'container': 'FLV', 'video_resolution': '360p',
         'video_encoding': 'H.264', 'video_profile': 'Main', 'video_bitrate': '0.5',
         'audio_encoding': 'AAC', 'audio_bitrate': '128'},
        #{'itag': '82', 'container': 'MP4', 'video_resolution': '360p', 'video_encoding': 'H.264', 'video_profile': '3D', 'video_bitrate': '0.5', 'audio_encoding': 'AAC', 'audio_bitrate': '96'},
        {'itag': '18', 'container': 'MP4', 'video_resolution': '360p',
         'video_encoding': 'H.264', 'video_profile': 'Baseline', 'video_bitrate': '0.5',
         'audio_encoding': 'AAC', 'audio_bitrate': '96'},
        {'itag': '6', 'container': 'FLV', 'video_resolution': '270p',
         'video_encoding': 'Sorenson H.263', 'video_profile': '', 'video_bitrate': '0.8',
         'audio_encoding': 'MP3', 'audio_bitrate': '64'},
        #{'itag': '83', 'container': 'MP4', 'video_resolution': '240p', 'video_encoding': 'H.264', 'video_profile': '3D', 'video_bitrate': '0.5', 'audio_encoding': 'AAC', 'audio_bitrate': '96'},
        {'itag': '13', 'container': '3GP', 'video_resolution': '',
         'video_encoding': 'MPEG-4 Visual', 'video_profile': '', 'video_bitrate': '0.5',
         'audio_encoding': 'AAC', 'audio_bitrate': ''},
        {'itag': '5', 'container': 'FLV', 'video_resolution': '240p',
         'video_encoding': 'Sorenson H.263', 'video_profile': '', 'video_bitrate': '0.25',
         'audio_encoding': 'MP3', 'audio_bitrate': '64'},
        {'itag': '36', 'container': '3GP', 'video_resolution': '240p',
         'video_encoding': 'MPEG-4 Visual', 'video_profile': 'Simple', 'video_bitrate': '0.175',
         'audio_encoding': 'AAC', 'audio_bitrate': '32'},
        {'itag': '17', 'container': '3GP', 'video_resolution': '144p',
         'video_encoding': 'MPEG-4 Visual', 'video_profile': 'Simple', 'video_bitrate': '0.05',
         'audio_encoding': 'AAC', 'audio_bitrate': '24'},
    ]

    def s_to_sig(js, s):
        # Examples:
        # - https://www.youtube.com/yts/jsbin/player-da_DK-vflWlK-zq/base.js
        # - https://www.youtube.com/yts/jsbin/player-vflvABTsY/da_DK/base.js
        # - https://www.youtube.com/yts/jsbin/player-vfls4aurX/da_DK/base.js
        # - https://www.youtube.com/yts/jsbin/player_ias-vfl_RGK2l/en_US/base.js
        # - https://www.youtube.com/yts/jsbin/player-vflRjqq_w/da_DK/base.js
        # - https://www.youtube.com/yts/jsbin/player_ias-vfl-jbnrr/da_DK/base.js
        def tr_js(code):
            code = re.sub(r'function', r'def', code)
            code = re.sub(r'(\W)(as|if|in|is|or)\(', r'\1_\2(', code)
            code = re.sub(r'\$', '_dollar', code)
            code = re.sub(r'\{', r':\n\t', code)
            code = re.sub(r'\}', r'\n', code)
            code = re.sub(r'var\s+', r'', code)
            code = re.sub(r'(\w+).join\(""\)', r'"".join(\1)', code)
            code = re.sub(r'(\w+).length', r'len(\1)', code)
            code = re.sub(r'(\w+).slice\((\w+)\)', r'\1[\2:]', code)
            code = re.sub(r'(\w+).splice\((\w+),(\w+)\)', r'del \1[\2:\2+\3]', code)
            code = re.sub(r'(\w+).split\(""\)', r'list(\1)', code)
            return code

        js = js.replace('\n', ' ')
        f1 = match1(js, r'\.set\(\w+\.sp,encodeURIComponent\(([$\w]+)') or \
            match1(js, r'\.set\(\w+\.sp,\(0,window\.encodeURIComponent\)\(([$\w]+)') or \
            match1(js, r'\.set\(\w+\.sp,([$\w]+)\(\w+\.s\)\)') or \
            match1(js, r'"signature",([$\w]+)\(\w+\.\w+\)') or \
            match1(js, r'=([$\w]+)\(decodeURIComponent\(')
        f1def = match1(js, r'function %s(\(\w+\)\{[^\{]+\})' % re.escape(f1)) or \
                match1(js, r'\W%s=function(\(\w+\)\{[^\{]+\})' % re.escape(f1))
        f1def = re.sub(r'([$\w]+\.)([$\w]+\(\w+,\d+\))', r'\2', f1def)
        f1def = 'function main_%s%s' % (f1, f1def)  # prefix to avoid potential namespace conflict
        code = tr_js(f1def)
        f2s = set(re.findall(r'([$\w]+)\(\w+,\d+\)', f1def))
        for f2 in f2s:
            f2e = re.escape(f2)
            f2def = re.search(r'[^$\w]%s:function\((\w+,\w+)\)(\{[^\{\}]+\})' % f2e, js)
            if f2def:
                f2def = 'function {}({}){}'.format(f2e, f2def.group(1), f2def.group(2))
            else:
                f2def = re.search(r'[^$\w]%s:function\((\w+)\)(\{[^\{\}]+\})' % f2e, js)
                f2def = 'function {}({},b){}'.format(f2e, f2def.group(1), f2def.group(2))
            f2 = re.sub(r'(as|if|in|is|or)', r'_\1', f2)
            f2 = re.sub(r'\$', '_dollar', f2)
            code = code + 'global %s\n' % f2 + tr_js(f2def)

        f1 = re.sub(r'(as|if|in|is|or)', r'_\1', f1)
        f1 = re.sub(r'\$', '_dollar', f1)
        code = code + 'sig=main_%s(s)' % f1  # prefix to avoid potential namespace conflict
        exec(code, globals(), locals())
        return locals()['sig']

    def chunk_by_range(url, size):
        urls = []
        chunk_size = 10485760
        start, end = 0, chunk_size - 1
        urls.append('%s&range=%s-%s' % (url, start, end))
        while end + 1 < size:  # processed size < expected size
            start, end = end + 1, end + chunk_size
            urls.append('%s&range=%s-%s' % (url, start, end))
        return urls

    def get_url_from_vid(vid):
        return 'https://youtu.be/{}'.format(vid)

    def get_vid_from_url(url):
        """Extracts video ID from URL.
        """
        return match1(url, r'youtu\.be/([^?/]+)') or \
          match1(url, r'youtube\.com/embed/([^/?]+)') or \
          match1(url, r'youtube\.com/v/([^/?]+)') or \
          match1(url, r'youtube\.com/watch/([^/?]+)') or \
          parse_query_param(url, 'v') or \
          parse_query_param(parse_query_param(url, 'u'), 'v')

    def get_playlist_id_from_url(url):
        """Extracts playlist ID from URL.
        """
        return parse_query_param(url, 'list') or \
          parse_query_param(url, 'p')

    def download_playlist_by_url(self, url, **kwargs):
        self.url = url

        playlist_id = self.__class__.get_playlist_id_from_url(self.url)
        if playlist_id is None:
            log.wtf('[Failed] Unsupported URL pattern.')

        video_page = get_content('https://www.youtube.com/playlist?list=%s' % playlist_id)
        playlist_json_serialized = match1(video_page, r'window\["ytInitialData"\]\s*=\s*(.+);', r'var\s+ytInitialData\s*=\s*([^;]+);')

        if len(playlist_json_serialized) == 0:
            log.wtf('[Failed] Unable to extract playlist data')

        ytInitialData = json.loads(playlist_json_serialized[0])

        tab0 = ytInitialData['contents']['twoColumnBrowseResultsRenderer']['tabs'][0]
        itemSection0 = tab0['tabRenderer']['content']['sectionListRenderer']['contents'][0]
        playlistVideoList0 = itemSection0['itemSectionRenderer']['contents'][0]
        videos = playlistVideoList0['playlistVideoListRenderer']['contents']

        self.title = re.search(r'<meta name="title" content="([^"]+)"', video_page).group(1)
        self.p_playlist()
        for index, video in enumerate(videos, 1):
            vid = video['playlistVideoRenderer']['videoId']
            try:
                self.__class__().download_by_url(self.__class__.get_url_from_vid(vid), index=index, **kwargs)
            except:
                pass
        # FIXME: show DASH stream sizes (by default) for playlist videos

    def prepare(self, **kwargs):
        assert self.url or self.vid

        if not self.vid and self.url:
            self.vid = self.__class__.get_vid_from_url(self.url)

            if self.vid is None:
                self.download_playlist_by_url(self.url, **kwargs)
                exit(0)

        if re.search('\Wlist=', self.url) and not kwargs.get('playlist'):
            log.w('This video is from a playlist. (use --playlist to download all videos in the playlist.)')

        # Get video info
        # 'eurl' is a magic parameter that can bypass age restriction
        # full form: 'eurl=https%3A%2F%2Fyoutube.googleapis.com%2Fv%2F{VIDEO_ID}'
        video_info = parse.parse_qs(get_content('https://www.youtube.com/get_video_info?video_id={}&eurl=https%3A%2F%2Fy'.format(self.vid)))
        logging.debug('STATUS: %s' % video_info['status'][0])

        ytplayer_config = None
        if 'status' not in video_info:
            log.wtf('[Failed] Unknown status.', exit_code=None)
            raise
        elif video_info['status'] == ['ok']:
            if 'use_cipher_signature' not in video_info or video_info['use_cipher_signature'] == ['False']:
                self.title = parse.unquote_plus(json.loads(video_info["player_response"][0])["videoDetails"]["title"])
                # Parse video page (for DASH)
                video_page = get_content('https://www.youtube.com/watch?v=%s' % self.vid)
                try:
                    try:
                        # Complete ytplayer_config
                        ytplayer_config = json.loads(re.search('ytplayer.config\s*=\s*([^\n]+?});', video_page).group(1))

                        # Workaround: get_video_info returns bad s. Why?
                        if 'url_encoded_fmt_stream_map' not in ytplayer_config['args']:
                            stream_list = json.loads(ytplayer_config['args']['player_response'])['streamingData']['formats']
                        else:
                            stream_list = ytplayer_config['args']['url_encoded_fmt_stream_map'].split(',')
                        #stream_list = ytplayer_config['args']['adaptive_fmts'].split(',')

                        if 'assets' in ytplayer_config:
                            self.html5player = 'https://www.youtube.com' + ytplayer_config['assets']['js']
                        elif re.search('([^"]*/base\.js)"', video_page):
                            self.html5player = 'https://www.youtube.com' + re.search('([^"]*/base\.js)"', video_page).group(1)
                            self.html5player = self.html5player.replace('\/', '/') # unescape URL
                        else:
                            self.html5player = None

                    except:
                        # ytplayer_config = {args:{raw_player_response:ytInitialPlayerResponse}}
                        ytInitialPlayerResponse = json.loads(re.search('ytInitialPlayerResponse\s*=\s*([^\n]+?});', video_page).group(1))

                        stream_list = ytInitialPlayerResponse['streamingData']['formats']
                        #stream_list = ytInitialPlayerResponse['streamingData']['adaptiveFormats']

                        if re.search('([^"]*/base\.js)"', video_page):
                            self.html5player = 'https://www.youtube.com' + re.search('([^"]*/base\.js)"', video_page).group(1)
                        else:
                            self.html5player = None

                except:
                    if 'url_encoded_fmt_stream_map' not in video_info:
                        stream_list = json.loads(video_info['player_response'][0])['streamingData']['formats']
                    else:
                        stream_list = video_info['url_encoded_fmt_stream_map'][0].split(',')

                    if re.search('([^"]*/base\.js)"', video_page):
                        self.html5player = 'https://www.youtube.com' + re.search('([^"]*/base\.js)"', video_page).group(1)
                    else:
                        self.html5player = None

            else:
                # Parse video page instead
                video_page = get_content('https://www.youtube.com/watch?v=%s' % self.vid)
                ytplayer_config = json.loads(re.search('ytplayer.config\s*=\s*([^\n]+?});', video_page).group(1))

                self.title = json.loads(ytplayer_config["args"]["player_response"])["videoDetails"]["title"]
                self.html5player = 'https://www.youtube.com' + ytplayer_config['assets']['js']
                stream_list = ytplayer_config['args']['url_encoded_fmt_stream_map'].split(',')

        elif video_info['status'] == ['fail']:
            logging.debug('ERRORCODE: %s' % video_info['errorcode'][0])
            if video_info['errorcode'] == ['150']:
                # FIXME: still relevant?
                if cookies:
                    # Load necessary cookies into headers (for age-restricted videos)
                    consent, ssid, hsid, sid = 'YES', '', '', ''
                    for cookie in cookies:
                        if cookie.domain.endswith('.youtube.com'):
                            if cookie.name == 'SSID':
                                ssid = cookie.value
                            elif cookie.name == 'HSID':
                                hsid = cookie.value
                            elif cookie.name == 'SID':
                                sid = cookie.value
                    cookie_str = 'CONSENT=%s; SSID=%s; HSID=%s; SID=%s' % (consent, ssid, hsid, sid)

                    video_page = get_content('https://www.youtube.com/watch?v=%s' % self.vid,
                                             headers={'Cookie': cookie_str})
                else:
                    video_page = get_content('https://www.youtube.com/watch?v=%s' % self.vid)

                try:
                    ytplayer_config = json.loads(re.search('ytplayer.config\s*=\s*([^\n]+});ytplayer', video_page).group(1))
                except:
                    msg = re.search('class="message">([^<]+)<', video_page).group(1)
                    log.wtf('[Failed] Got message "%s". Try to login with --cookies.' % msg.strip())

                if 'title' in ytplayer_config['args']:
                    # 150 Restricted from playback on certain sites
                    # Parse video page instead
                    self.title = ytplayer_config['args']['title']
                    self.html5player = 'https://www.youtube.com' + ytplayer_config['assets']['js']
                    stream_list = ytplayer_config['args']['url_encoded_fmt_stream_map'].split(',')
                else:
                    log.wtf('[Error] The uploader has not made this video available in your country.', exit_code=None)
                    raise
                    #self.title = re.search('<meta name="title" content="([^"]+)"', video_page).group(1)
                    #stream_list = []

            elif video_info['errorcode'] == ['100']:
                log.wtf('[Failed] This video does not exist.', exit_code=None) #int(video_info['errorcode'][0])
                raise

            else:
                log.wtf('[Failed] %s' % video_info['reason'][0], exit_code=None) #int(video_info['errorcode'][0])
                raise

        else:
            log.wtf('[Failed] Invalid status.', exit_code=None)
            raise

        # YouTube Live
        if ytplayer_config and (ytplayer_config['args'].get('livestream') == '1' or ytplayer_config['args'].get('live_playback') == '1'):
            if 'hlsvp' in ytplayer_config['args']:
                hlsvp = ytplayer_config['args']['hlsvp']
            else:
                player_response= json.loads(ytplayer_config['args']['player_response'])
                log.e('[Failed] %s' % player_response['playabilityStatus']['reason'], exit_code=1)

            if 'info_only' in kwargs and kwargs['info_only']:
                return
            else:
                download_url_ffmpeg(hlsvp, self.title, 'mp4')
                exit(0)

        for stream in stream_list:
            if isinstance(stream, str):
                metadata = parse.parse_qs(stream)
                stream_itag = metadata['itag'][0]
                self.streams[stream_itag] = {
                    'itag': metadata['itag'][0],
                    'url': metadata['url'][0],
                    'sig': metadata['sig'][0] if 'sig' in metadata else None,
                    's': metadata['s'][0] if 's' in metadata else None,
                    'quality': metadata['quality'][0] if 'quality' in metadata else None,
                    #'quality': metadata['quality_label'][0] if 'quality_label' in metadata else None,
                    'type': metadata['type'][0],
                    'mime': metadata['type'][0].split(';')[0],
                    'container': mime_to_container(metadata['type'][0].split(';')[0]),
                }
            else:
                stream_itag = str(stream['itag'])
                self.streams[stream_itag] = {
                    'itag': str(stream['itag']),
                    'url': stream['url'] if 'url' in stream else None,
                    'sig': None,
                    's': None,
                    'quality': stream['quality'],
                    'type': stream['mimeType'],
                    'mime': stream['mimeType'].split(';')[0],
                    'container': mime_to_container(stream['mimeType'].split(';')[0]),
                }
                if 'signatureCipher' in stream:
                    self.streams[stream_itag].update(dict([(_.split('=')[0], parse.unquote(_.split('=')[1]))
                                                           for _ in stream['signatureCipher'].split('&')]))

        # Prepare caption tracks
        try:
            try:
                caption_tracks = json.loads(ytplayer_config['args']['player_response'])['captions']['playerCaptionsTracklistRenderer']['captionTracks']
            except:
                caption_tracks = ytInitialPlayerResponse['captions']['playerCaptionsTracklistRenderer']['captionTracks']
            for ct in caption_tracks:
                ttsurl, lang = ct['baseUrl'], ct['languageCode']

                tts_xml = parseString(get_content(ttsurl))
                transcript = tts_xml.getElementsByTagName('transcript')[0]
                texts = transcript.getElementsByTagName('text')
                srt = ""; seq = 0
                for text in texts:
                    if text.firstChild is None: continue # empty element
                    seq += 1
                    start = float(text.getAttribute('start'))
                    if text.getAttribute('dur'):
                        dur = float(text.getAttribute('dur'))
                    else: dur = 1.0 # could be ill-formed XML
                    finish = start + dur
                    m, s = divmod(start, 60); h, m = divmod(m, 60)
                    start = '{:0>2}:{:0>2}:{:06.3f}'.format(int(h), int(m), s).replace('.', ',')
                    m, s = divmod(finish, 60); h, m = divmod(m, 60)
                    finish = '{:0>2}:{:0>2}:{:06.3f}'.format(int(h), int(m), s).replace('.', ',')
                    content = unescape_html(text.firstChild.nodeValue)

                    srt += '%s\n' % str(seq)
                    srt += '%s --> %s\n' % (start, finish)
                    srt += '%s\n\n' % content

                self.caption_tracks[lang] = srt
        except: pass

        # Prepare DASH streams (NOTE: not every video has DASH streams!)
        try:
            dashmpd = ytplayer_config['args']['dashmpd']
            dash_xml = parseString(get_content(dashmpd))
            for aset in dash_xml.getElementsByTagName('AdaptationSet'):
                mimeType = aset.getAttribute('mimeType')
                if mimeType == 'audio/mp4':
                    rep = aset.getElementsByTagName('Representation')[-1]
                    burls = rep.getElementsByTagName('BaseURL')
                    dash_mp4_a_url = burls[0].firstChild.nodeValue
                    dash_mp4_a_size = burls[0].getAttribute('yt:contentLength')
                    if not dash_mp4_a_size:
                        try: dash_mp4_a_size = url_size(dash_mp4_a_url)
                        except: continue
                elif mimeType == 'audio/webm':
                    rep = aset.getElementsByTagName('Representation')[-1]
                    burls = rep.getElementsByTagName('BaseURL')
                    dash_webm_a_url = burls[0].firstChild.nodeValue
                    dash_webm_a_size = burls[0].getAttribute('yt:contentLength')
                    if not dash_webm_a_size:
                        try: dash_webm_a_size = url_size(dash_webm_a_url)
                        except: continue
                elif mimeType == 'video/mp4':
                    for rep in aset.getElementsByTagName('Representation'):
                        w = int(rep.getAttribute('width'))
                        h = int(rep.getAttribute('height'))
                        itag = rep.getAttribute('id')
                        burls = rep.getElementsByTagName('BaseURL')
                        dash_url = burls[0].firstChild.nodeValue
                        dash_size = burls[0].getAttribute('yt:contentLength')
                        if not dash_size:
                            try: dash_size = url_size(dash_url)
                            except: continue
                        dash_urls = self.__class__.chunk_by_range(dash_url, int(dash_size))
                        dash_mp4_a_urls = self.__class__.chunk_by_range(dash_mp4_a_url, int(dash_mp4_a_size))
                        self.dash_streams[itag] = {
                            'quality': '%sx%s' % (w, h),
                            'itag': itag,
                            'type': mimeType,
                            'mime': mimeType,
                            'container': 'mp4',
                            'src': [dash_urls, dash_mp4_a_urls],
                            'size': int(dash_size) + int(dash_mp4_a_size)
                        }
                elif mimeType == 'video/webm':
                    for rep in aset.getElementsByTagName('Representation'):
                        w = int(rep.getAttribute('width'))
                        h = int(rep.getAttribute('height'))
                        itag = rep.getAttribute('id')
                        burls = rep.getElementsByTagName('BaseURL')
                        dash_url = burls[0].firstChild.nodeValue
                        dash_size = burls[0].getAttribute('yt:contentLength')
                        if not dash_size:
                            try: dash_size = url_size(dash_url)
                            except: continue
                        dash_urls = self.__class__.chunk_by_range(dash_url, int(dash_size))
                        dash_webm_a_urls = self.__class__.chunk_by_range(dash_webm_a_url, int(dash_webm_a_size))
                        self.dash_streams[itag] = {
                            'quality': '%sx%s' % (w, h),
                            'itag': itag,
                            'type': mimeType,
                            'mime': mimeType,
                            'container': 'webm',
                            'src': [dash_urls, dash_webm_a_urls],
                            'size': int(dash_size) + int(dash_webm_a_size)
                        }
        except:
            # VEVO
            if not self.html5player: return
            self.html5player = self.html5player.replace('\/', '/') # unescape URL (for age-restricted videos)
            self.js = get_content(self.html5player)

            try:
                # Video info from video page (not always available)
                streams = [dict([(i.split('=')[0],
                                  parse.unquote(i.split('=')[1]))
                                 for i in afmt.split('&')])
                           for afmt in ytplayer_config['args']['adaptive_fmts'].split(',')]
            except:
                if 'adaptive_fmts' in video_info:
                    streams = [dict([(i.split('=')[0],
                                      parse.unquote(i.split('=')[1]))
                                     for i in afmt.split('&')])
                               for afmt in video_info['adaptive_fmts'][0].split(',')]
                else:
                    try:
                        try:
                            streams = json.loads(video_info['player_response'][0])['streamingData']['adaptiveFormats']
                        except:
                            streams = ytInitialPlayerResponse['streamingData']['adaptiveFormats']
                    except:  # no DASH stream at all
                        return

                    # streams without contentLength got broken urls, just remove them (#2767)
                    streams = [stream for stream in streams if 'contentLength' in stream]

                    for stream in streams:
                        stream['itag'] = str(stream['itag'])
                        if 'qualityLabel' in stream:
                            stream['quality_label'] = stream['qualityLabel']
                            del stream['qualityLabel']
                        if 'width' in stream:
                            stream['size'] = '{}x{}'.format(stream['width'], stream['height'])
                            del stream['width']
                            del stream['height']
                        stream['type'] = stream['mimeType']
                        stream['clen'] = stream['contentLength']
                        stream['init'] = '{}-{}'.format(
                            stream['initRange']['start'],
                            stream['initRange']['end'])
                        stream['index'] = '{}-{}'.format(
                            stream['indexRange']['start'],
                            stream['indexRange']['end'])
                        del stream['mimeType']
                        del stream['contentLength']
                        del stream['initRange']
                        del stream['indexRange']
                        if 'signatureCipher' in stream:
                            stream.update(dict([(_.split('=')[0], parse.unquote(_.split('=')[1]))
                                                for _ in stream['signatureCipher'].split('&')]))
                            del stream['signatureCipher']

            for stream in streams: # get over speed limiting
                stream['url'] += '&ratebypass=yes'
            for stream in streams: # audio
                if stream['type'].startswith('audio/mp4'):
                    dash_mp4_a_url = stream['url']
                    if 's' in stream:
                        sig = self.__class__.s_to_sig(self.js, stream['s'])
                        dash_mp4_a_url += '&sig={}'.format(sig)
                    dash_mp4_a_size = stream['clen']
                elif stream['type'].startswith('audio/webm'):
                    dash_webm_a_url = stream['url']
                    if 's' in stream:
                        sig = self.__class__.s_to_sig(self.js, stream['s'])
                        dash_webm_a_url += '&sig={}'.format(sig)
                    dash_webm_a_size = stream['clen']
            for stream in streams: # video
                if 'size' in stream:
                    if stream['type'].startswith('video/mp4'):
                        mimeType = 'video/mp4'
                        dash_url = stream['url']
                        if 's' in stream:
                            sig = self.__class__.s_to_sig(self.js, stream['s'])
                            dash_url += '&sig={}'.format(sig)
                        dash_size = stream['clen']
                        itag = stream['itag']
                        dash_urls = self.__class__.chunk_by_range(dash_url, int(dash_size))
                        dash_mp4_a_urls = self.__class__.chunk_by_range(dash_mp4_a_url, int(dash_mp4_a_size))
                        self.dash_streams[itag] = {
                            'quality': '%s (%s)' % (stream['size'], stream['quality_label']),
                            'itag': itag,
                            'type': mimeType,
                            'mime': mimeType,
                            'container': 'mp4',
                            'src': [dash_urls, dash_mp4_a_urls],
                            'size': int(dash_size) + int(dash_mp4_a_size)
                        }
                    elif stream['type'].startswith('video/webm'):
                        mimeType = 'video/webm'
                        dash_url = stream['url']
                        if 's' in stream:
                            sig = self.__class__.s_to_sig(self.js, stream['s'])
                            dash_url += '&sig={}'.format(sig)
                        dash_size = stream['clen']
                        itag = stream['itag']
                        audio_url = None
                        audio_size = None
                        try:
                            audio_url = dash_webm_a_url
                            audio_size = int(dash_webm_a_size)
                        except UnboundLocalError as e:
                            audio_url = dash_mp4_a_url
                            audio_size = int(dash_mp4_a_size)
                        dash_urls = self.__class__.chunk_by_range(dash_url, int(dash_size))
                        audio_urls = self.__class__.chunk_by_range(audio_url, int(audio_size))
                        self.dash_streams[itag] = {
                            'quality': '%s (%s)' % (stream['size'], stream['quality_label']),
                            'itag': itag,
                            'type': mimeType,
                            'mime': mimeType,
                            'container': 'webm',
                            'src': [dash_urls, audio_urls],
                            'size': int(dash_size) + int(audio_size)
                        }

    def extract(self, **kwargs):
        if not self.streams_sorted:
            # No stream is available
            return

        if 'stream_id' in kwargs and kwargs['stream_id']:
            # Extract the stream
            stream_id = kwargs['stream_id']
            if stream_id not in self.streams and stream_id not in self.dash_streams:
                log.e('[Error] Invalid video format.')
                log.e('Run \'-i\' command with no specific video format to view all available formats.')
                exit(2)
        else:
            # Extract stream with the best quality
            stream_id = self.streams_sorted[0]['itag']

        if stream_id in self.streams:
            src = self.streams[stream_id]['url']
            if self.streams[stream_id]['sig'] is not None:
                sig = self.streams[stream_id]['sig']
                src += '&sig={}'.format(sig)
            elif self.streams[stream_id]['s'] is not None:
                if not hasattr(self, 'js'):
                    self.js = get_content(self.html5player)
                s = self.streams[stream_id]['s']
                sig = self.__class__.s_to_sig(self.js, s)
                src += '&sig={}'.format(sig)

            self.streams[stream_id]['src'] = [src]
            self.streams[stream_id]['size'] = urls_size(self.streams[stream_id]['src'])

site = YouTube()
download = site.download_by_url
download_playlist = site.download_playlist_by_url
