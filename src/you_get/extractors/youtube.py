#!/usr/bin/env python

from ..common import *
from ..extractor import VideoExtractor

try:
    import dukpy
except ImportError:
    log.e('Please install dukpy in order to extract videos from YouTube:')
    log.e('$ pip install dukpy')
    exit(0)
from urllib.parse import urlparse, parse_qs, urlencode
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

    def dethrottle(js, url):
        def n_to_n(js, n):
            # Examples:
            #   yma - https://www.youtube.com/s/player/84314bef/player_ias.vflset/en_US/base.js
            #   Xka - https://www.youtube.com/s/player/dc0c6770/player_ias.vflset/sv_SE/base.js
            #   jma - https://www.youtube.com/s/player/8d9f6215/player_ias.vflset/sv_SE/base.js
            f1 = match1(js, r',[$\w]+\.length\|\|([$\w]+)\(""\)\)}};')
            f1def = match1(js, r'\W%s=(function\(\w+\).+?\)});' % re.escape(f1))
            n = dukpy.evaljs('(%s)("%s")' % (f1def, n))
            return n

        u = urlparse(url)
        qs = parse_qs(u.query)
        n = n_to_n(js, qs['n'][0])
        qs['n'] = [n]
        return u._replace(query=urlencode(qs, doseq=True)).geturl()

    def s_to_sig(js, s):
        # Examples:
        #   BPa - https://www.youtube.com/s/player/84314bef/player_ias.vflset/en_US/base.js
        #   Xva - https://www.youtube.com/s/player/dc0c6770/player_ias.vflset/sv_SE/base.js
        js_code = ''
        f1 = match1(js, r'=([$\w]+)\(decodeURIComponent\(')
        f1def = match1(js, r'\W%s=function(\(\w+\)\{[^\{]+\})' % re.escape(f1))
        f1def = re.sub(r'([$\w]+\.)([$\w]+\(\w+,\d+\))', r'\2', f1def)  # remove . prefix
        f1def = 'function %s%s' % (f1, f1def)
        f2s = set(re.findall(r'([$\w]+)\(\w+,\d+\)', f1def))  # find all invoked function names
        for f2 in f2s:
            f2e = re.escape(f2)
            f2def = re.search(r'[^$\w]%s:function\((\w+,\w+)\)(\{[^\{\}]+\})' % f2e, js)
            if f2def:
                f2def = 'function {}({}){}'.format(f2e, f2def.group(1), f2def.group(2))
            else:
                f2def = re.search(r'[^$\w]%s:function\((\w+)\)(\{[^\{\}]+\})' % f2e, js)
                f2def = 'function {}({},b){}'.format(f2e, f2def.group(1), f2def.group(2))
            js_code += f2def + ';'
        js_code += f1def + ';%s("%s")' % (f1, s)
        sig = dukpy.evaljs(js_code)
        return sig

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
          match1(url, r'youtube\.com/shorts/([^/?]+)') or \
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

    def check_playability_response(self, ytInitialPlayerResponse):
        STATUS_OK = "OK"

        playerResponseStatus = ytInitialPlayerResponse["playabilityStatus"]["status"]
        if playerResponseStatus != STATUS_OK:
            reason = ytInitialPlayerResponse["playabilityStatus"].get("reason", "")
            raise AssertionError(
                f"Server refused to provide video details. Returned status: {playerResponseStatus}, reason: {reason}."
            )

    def prepare(self, **kwargs):
        self.ua = 'Mozilla/5.0 (Linux; Android 14) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.6533.103 Mobile Safari/537.36'

        assert self.url or self.vid

        if not self.vid and self.url:
            self.vid = self.__class__.get_vid_from_url(self.url)

            if self.vid is None:
                self.download_playlist_by_url(self.url, **kwargs)
                exit(0)

        if re.search(r'\Wlist=', self.url) and not kwargs.get('playlist'):
            log.w('This video is from a playlist. (use --playlist to download all videos in the playlist.)')

        # Extract from video page
        logging.debug('Extracting from the video page...')
        video_page = get_content('https://www.youtube.com/watch?v=%s' % self.vid, headers={'User-Agent': self.ua})

        try:
            jsUrl = re.search(r'([^"]*/base\.js)"', video_page).group(1)
        except:
            log.wtf('[Failed] Unable to find base.js on the video page')
        self.html5player = 'https://www.youtube.com' + jsUrl
        logging.debug('Retrieving the player code...')
        self.js = get_content(self.html5player).replace('\n', ' ')

        logging.debug('Loading ytInitialPlayerResponse...')
        ytInitialPlayerResponse = json.loads(re.search(r'ytInitialPlayerResponse\s*=\s*([^\n]+?});(\n|</script>|var )', video_page).group(1))
        self.check_playability_response(ytInitialPlayerResponse)

        # Get the video title
        self.title = ytInitialPlayerResponse["videoDetails"]["title"]

        # Check the status
        playabilityStatus = ytInitialPlayerResponse['playabilityStatus']
        status = playabilityStatus['status']
        logging.debug('status: %s' % status)
        if status != 'OK':
            # If cookies are loaded, status should be OK
            try:
                subreason = playabilityStatus['errorScreen']['playerErrorMessageRenderer']['subreason']['runs'][0]['text']
                log.e('[Error] %s (%s)' % (playabilityStatus['reason'], subreason))
            except:
                log.e('[Error] %s' % playabilityStatus['reason'])
            if status == 'LOGIN_REQUIRED':
                log.e('View the video from a browser and export the cookies, then use --cookies to load cookies.')
            exit(1)

        stream_list = ytInitialPlayerResponse['streamingData']['formats']

        for stream in stream_list:
            logging.debug('Found format: itag=%s' % stream['itag'])
            if 'signatureCipher' in stream:
                logging.debug('  Parsing signatureCipher for itag=%s...' % stream['itag'])
                qs = parse_qs(stream['signatureCipher'])
                #logging.debug(qs)
                sp = qs['sp'][0]
                sig = self.__class__.s_to_sig(self.js, qs['s'][0])
                url = qs['url'][0] + '&{}={}'.format(sp, sig)
            elif 'url' in stream:
                url = stream['url']
            else:
                log.wtf('  No signatureCipher or url for itag=%s' % stream['itag'])
            url = self.__class__.dethrottle(self.js, url)

            self.streams[str(stream['itag'])] = {
                'itag': str(stream['itag']),
                'url': url,
                'quality': stream['quality'],
                'type': stream['mimeType'],
                'mime': stream['mimeType'].split(';')[0],
                'container': mime_to_container(stream['mimeType'].split(';')[0]),
            }

        # FIXME: Prepare caption tracks
        try:
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

                if 'kind' in ct:
                    self.caption_tracks[ct['vssId']] = srt  # autogenerated
                else:
                    self.caption_tracks[lang] = srt
        except: pass

        # Prepare DASH streams
        if 'adaptiveFormats' in ytInitialPlayerResponse['streamingData']:
            streams = ytInitialPlayerResponse['streamingData']['adaptiveFormats']

            # FIXME: dead code?
            # streams without contentLength got broken urls, just remove them (#2767)
            streams = [stream for stream in streams if 'contentLength' in stream]

            for stream in streams:
                logging.debug('Found adaptiveFormat: itag=%s' % stream['itag'])
                stream['itag'] = str(stream['itag'])
                if 'qualityLabel' in stream:
                    stream['quality_label'] = stream['qualityLabel']
                    del stream['qualityLabel']
                    logging.debug('  quality_label: \t%s' % stream['quality_label'])
                if 'width' in stream:
                    stream['size'] = '{}x{}'.format(stream['width'], stream['height'])
                    del stream['width']
                    del stream['height']
                    logging.debug('  size: \t%s' % stream['size'])
                stream['type'] = stream['mimeType']
                logging.debug('  type: \t%s' % stream['type'])
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
                    logging.debug('  Parsing signatureCipher for itag=%s...' % stream['itag'])
                    qs = parse_qs(stream['signatureCipher'])
                    #logging.debug(qs)
                    sp = qs['sp'][0]
                    sig = self.__class__.s_to_sig(self.js, qs['s'][0])
                    url = qs['url'][0] + '&ratebypass=yes&{}={}'.format(sp, sig)
                elif 'url' in stream:
                    url = stream['url']
                else:
                    log.wtf('No signatureCipher or url for itag=%s' % stream['itag'])
                url = self.__class__.dethrottle(self.js, url)
                stream['url'] = url

            for stream in streams: # audio
                if stream['type'].startswith('audio/mp4'):
                    dash_mp4_a_url = stream['url']
                    dash_mp4_a_size = stream['clen']
                elif stream['type'].startswith('audio/webm'):
                    dash_webm_a_url = stream['url']
                    dash_webm_a_size = stream['clen']
            for stream in streams: # video
                if 'size' in stream:
                    if stream['type'].startswith('video/mp4'):
                        mimeType = 'video/mp4'
                        dash_url = stream['url']
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

            self.streams[stream_id]['src'] = [src]
            self.streams[stream_id]['size'] = urls_size(self.streams[stream_id]['src'])

site = YouTube()
download = site.download_by_url
download_playlist = site.download_playlist_by_url
