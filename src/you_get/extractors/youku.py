#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..common import *
from ..extractor import VideoExtractor

import base64
import ssl
import time
import traceback
import json
import math
from urllib import parse

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
        {'id': '3gphd',  'container': '3gp', 'video_profile': '标清（3GP）'},
    ]

    f_code_1 = 'becaf9be'
    f_code_2 = 'bf7e5f01'

    ctype = 12  #differ from 86

    def trans_e(a, c):
        """str, str->str
        This is an RC4 encryption."""
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

    def generate_ep(self, fileid, sid, token):
        ep = parse.quote(base64.b64encode(
            ''.join(self.__class__.trans_e(
                self.f_code_2,  #use the 86 fcode if using 86
                sid + '_' + fileid + '_' + token)).encode('latin1')),
            safe='~()*!.\''
        )
        return ep

    # Obsolete -- used to parse m3u8 on pl.youku.com
    def parse_m3u8(m3u8):
        return re.findall(r'(http://[^?]+)\?ts_start=0', m3u8)

    def oset(xs):
        """Turns a list into an ordered set. (removes duplicates)"""
        mem = set()
        for x in xs:
            if x not in mem:
                mem.add(x)
        return mem

    def get_vid_from_url(url):
        """Extracts video ID from URL.
        """
        return match1(url, r'youku\.com/v_show/id_([a-zA-Z0-9=]+)') or \
          match1(url, r'player\.youku\.com/player\.php/sid/([a-zA-Z0-9=]+)/v\.swf') or \
          match1(url, r'loader\.swf\?VideoIDS=([a-zA-Z0-9=]+)') or \
          match1(url, r'player\.youku\.com/embed/([a-zA-Z0-9=]+)')

    @staticmethod
    def get_playlist_id_from_url(url):
        """Extracts playlist ID from URL.
        """
        return match1(url, r'list\.youku\.com/show/id_([a-zA-Z0-9=]+)')

    @staticmethod
    def get_albumlist_id_from_url(url):
        return match1(url, r'list\.youku\.com/albumlist/show/id_(\d+)\.html')

    @staticmethod
    def is_playlist_page(url):
        return re.match(r'https?://list\.youku\.com/show/id_[a-zA-Z0-9=]+\.html',
                        url) is not None

    @staticmethod
    def is_albumlist_page(url):
        return re.match(r'https?://list\.youku\.com/albumlist/show/id_\d+\.html',
                        url) is not None

    @staticmethod
    def get_json(url):
        components = list(parse.urlparse(url))
        query = components[4]
        fields = dict(parse.parse_qsl(query))
        fields['callback'] = fields.get('callback', 'callback')
        components[4] = parse.urlencode(fields)
        url = parse.urlunparse(components)

        jstr = match1(get_content(url), r'^[^\{]*(\{.*\})[^\}]*$')
        jdict = json.loads(jstr)
        assert jdict['error'] == 1 and jdict['message'] == 'success'
        return jdict

    @classmethod
    def get_vurls_of_playlist(cls, url):
        list_page = get_content(url)
        first_video_url = match1(list_page, r'href="//v\.youku\.com/wechatShare/\?' \
                          'url=(http://v\.youku\.com/v_show/id_[a-zA-Z0-9=]+\.html)')
        video_page = get_content(first_video_url)
        js = match1(video_page, r'PageConfig\s*=\s*(\{.*?\});')
        js = re.sub(r'(\w+)\s*:', r'"\1":', js)
        js = re.sub(r':\s*(?P<quotes>[\'`])(?P<str>.*?)(?P=quotes)\s*(?=[,}])',
                    r': "\g<str>"', js)
        page_config = json.loads(js)
        vurls = []

        if page_config['page']['type'] == 'Num':
            episodes_per_page = 100
            total_episodes = int(page_config['page']['totalepisodes'])
            total_pages = math.ceil(total_episodes / episodes_per_page)
            for pagenum in range(1, total_pages+1):
                url = 'http:{host}page/playlist/pm_{pm}_vid_{vid}_showid_{sid}' \
                        '_page_{pn}{v}'.format(
                            host    = page_config['homeHost'],
                            pm      = page_config['playmode'],
                            vid     = page_config['videoId'],
                            sid     = page_config['showid'],
                            pn      = pagenum,
                            v       = '_v_' + page_config['parentvideoid']
                                        if 'parentvideoid' in page_config else ''
                        )
                jdict = cls.get_json(url)
                html = re.sub(r'<h4>相关片段</h4>.*$', '', jdict['html'])
                vurls += ['http:' + h for h in re.findall(r'href="(.*?)"', html)]
        elif page_config['page']['type'] == 'Date':
            raise NotImplementedError()
        else:
            raise NotImplementedError()

        return vurls

    @classmethod
    def get_vurls_of_albumlist(cls, url):
        vurls = []

        bdid = cls.get_albumlist_id_from_url(url)
        ascending = 1
        domain_listpage = 'list.youku.com'
        bdpage = {'page': 1, 'size': 20, 'total': 0}

        while True:
            url = 'http://{domain}/albumlist/items?id={id}&page={p}&size={s}&ascending={a}'.format(
                domain  = domain_listpage,
                id      = bdid,
                p       = bdpage['page'],
                s       = bdpage['size'],
                a       = ascending
            )

            jdict = cls.get_json(url)
            vurls += ['http:' + h for h in re.findall(r'<ul\s+class="info-list">.*?href="(.*?)".*?</ul>',
                                                      jdict['html'])]
            bdpage['total'] = int(jdict['data']['total'])

            if bdpage['page'] * bdpage['size'] < bdpage['total']:
                bdpage['page'] += 1
            else:
                break

        return vurls

    def download_playlist_by_url(self, url, **kwargs):
        self.url = url

        if self.__class__.is_playlist_page(url):
            vurls = self.__class__.get_vurls_of_playlist(url)
        elif self.__class__.is_albumlist_page(url):
            vurls = self.__class__.get_vurls_of_albumlist(url)
        else:
            log.e('Unsupported URL: {}'.format(url))
            sys.exit(1)

        page = get_content(url)
        self.title = r1(r'<meta name="title" content="([^"]+)"', page) or \
                     r1(r'<title>([^<]+)', page)
        self.p_playlist()

        for index, url in enumerate(vurls):
            try:
                self.__class__().download_by_url(url, index=index, **kwargs)
            except KeyboardInterrupt:
                raise
            except:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                traceback.print_exception(exc_type, exc_value, exc_traceback)

    def prepare(self, **kwargs):
        # Hot-plug cookie handler
        ssl_context = request.HTTPSHandler(
            context=ssl.SSLContext(ssl.PROTOCOL_TLSv1))
        cookie_handler = request.HTTPCookieProcessor()
        if 'extractor_proxy' in kwargs and kwargs['extractor_proxy']:
            proxy = parse_host(kwargs['extractor_proxy'])
            proxy_handler = request.ProxyHandler({
                'http': '%s:%s' % proxy,
                'https': '%s:%s' % proxy,
            })
        else:
            proxy_handler = request.ProxyHandler({})
        if not request._opener:
            opener = request.build_opener(proxy_handler)
            request.install_opener(opener)
        for handler in (ssl_context, cookie_handler, proxy_handler):
            request._opener.add_handler(handler)
        request._opener.addheaders = [('Cookie','__ysuid={}'.format(time.time()))]

        assert self.url or self.vid

        if self.url and not self.vid:
            self.vid = self.__class__.get_vid_from_url(self.url)

            if self.vid is None:
                self.download_playlist_by_url(self.url, **kwargs)
                exit(0)

        #HACK!
        if 'api_url' in kwargs:
            api_url = kwargs['api_url']  #85
            api12_url = kwargs['api12_url']  #86
            self.ctype = kwargs['ctype']
            self.title = kwargs['title']

        else:
            api_url = 'http://play.youku.com/play/get.json?vid=%s&ct=10' % self.vid
            api12_url = 'http://play.youku.com/play/get.json?vid=%s&ct=12' % self.vid

        try:
            meta = json.loads(get_content(
                api_url,
                headers={'Referer': 'http://static.youku.com/'}
            ))
            meta12 = json.loads(get_content(
                api12_url,
                headers={'Referer': 'http://static.youku.com/'}
            ))
            data = meta['data']
            data12 = meta12['data']
            assert 'stream' in data
        except AssertionError:
            if 'error' in data:
                if data['error']['code'] == -202:
                    # Password protected
                    self.password_protected = True
                    self.password = input(log.sprint('Password: ', log.YELLOW))
                    api_url += '&pwd={}'.format(self.password)
                    api12_url += '&pwd={}'.format(self.password)
                    meta = json.loads(get_content(
                        api_url,
                        headers={'Referer': 'http://static.youku.com/'}
                    ))
                    meta12 = json.loads(get_content(
                        api12_url,
                        headers={'Referer': 'http://static.youku.com/'}
                    ))
                    data = meta['data']
                    data12 = meta12['data']
                else:
                    log.wtf('[Failed] ' + data['error']['note'])
            else:
                log.wtf('[Failed] Video not found.')

        if not self.title:  #86
            self.title = data['video']['title']
        self.ep = data12['security']['encrypt_string']
        self.ip = data12['security']['ip']

        if 'stream' not in data and self.password_protected:
            log.wtf('[Failed] Wrong password.')

        stream_types = dict([(i['id'], i) for i in self.stream_types])
        audio_lang = data['stream'][0]['audio_lang']

        for stream in data['stream']:
            stream_id = stream['stream_type']
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
                        }]
                    }
                else:
                    self.streams[stream_id]['size'] += stream['size']
                    self.streams[stream_id]['pieces'].append({
                        'segs': stream['segs']
                    })

        self.streams_fallback = {}
        for stream in data12['stream']:
            stream_id = stream['stream_type']
            if stream_id in stream_types and stream['audio_lang'] == audio_lang:
                if 'alias-of' in stream_types[stream_id]:
                    stream_id = stream_types[stream_id]['alias-of']

                if stream_id not in self.streams_fallback:
                    self.streams_fallback[stream_id] = {
                        'container': stream_types[stream_id]['container'],
                        'video_profile': stream_types[stream_id]['video_profile'],
                        'size': stream['size'],
                        'pieces': [{
                            'segs': stream['segs']
                        }]
                    }
                else:
                    self.streams_fallback[stream_id]['size'] += stream['size']
                    self.streams_fallback[stream_id]['pieces'].append({
                        'segs': stream['segs']
                    })

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

        e_code = self.__class__.trans_e(
            self.f_code_1,
            base64.b64decode(bytes(self.ep, 'ascii'))
        )
        sid, token = e_code.split('_')

        while True:
            try:
                ksegs = []
                pieces = self.streams[stream_id]['pieces']
                for piece in pieces:
                    segs = piece['segs']
                    seg_count = len(segs)
                    for no in range(0, seg_count):
                        k = segs[no]['key']
                        fileid = segs[no]['fileid']
                        if k == -1:
                            # we hit the paywall; stop here
                            log.w('Skipping %d out of %d segments due to paywall' %
                                  (seg_count - no, seg_count))
                            break
                        ep = self.__class__.generate_ep(self, fileid,
                                                        sid, token)
                        q = parse.urlencode(dict(
                            ctype = self.ctype,
                            ev    = 1,
                            K     = k,
                            ep    = parse.unquote(ep),
                            oip   = str(self.ip),
                            token = token,
                            yxon  = 1
                        ))
                        u = 'http://k.youku.com/player/getFlvPath/sid/{sid}_00' \
                            '/st/{container}/fileid/{fileid}?{q}'.format(
                                sid       = sid,
                                container = self.streams[stream_id]['container'],
                                fileid    = fileid,
                                q         = q
                            )
                        ksegs += [i['server'] for i in json.loads(get_content(u))]
            except error.HTTPError as e:
                # Use fallback stream data in case of HTTP 404
                log.e('[Error] ' + str(e))
                self.streams = {}
                self.streams = self.streams_fallback
            except KeyError:
                # Move on to next stream if best quality not available
                del self.streams_sorted[0]
                stream_id = self.streams_sorted[0]['id']
            else: break

        if not kwargs['info_only']:
            self.streams[stream_id]['src'] = ksegs

    def open_download_by_vid(self, client_id, vid, **kwargs):
        """self, str, str, **kwargs->None

        Arguments:
        client_id:        An ID per client. For now we only know Acfun's
                          such ID.

        vid:              An video ID for each video, starts with "C".

        kwargs['embsig']: Youku COOP's anti hotlinking.
                          For Acfun, an API call must be done to Acfun's
                          server, or the "playsign" of the content of sign_url
                          shall be empty.

        Misc:
        Override the original one with VideoExtractor.

        Author:
        Most of the credit are to @ERioK, who gave his POC.

        History:
        Jul.28.2016 Youku COOP now have anti hotlinking via embsig. """
        self.f_code_1 = '10ehfkbv'  #can be retrived by running r.translate with the keys and the list e
        self.f_code_2 = 'msjv7h2b'

        # as in VideoExtractor
        self.url = None
        self.vid = vid
        self.name = "优酷开放平台 (Youku COOP)"

        #A little bit of work before self.prepare

        #Change as Jul.28.2016 Youku COOP updates its platform to add ant hotlinking
        if kwargs['embsig']:
            sign_url = "https://api.youku.com/players/custom.json?client_id={client_id}&video_id={video_id}&embsig={embsig}".format(client_id = client_id, video_id = vid, embsig = kwargs['embsig'])
        else:
            sign_url = "https://api.youku.com/players/custom.json?client_id={client_id}&video_id={video_id}".format(client_id = client_id, video_id = vid)

        playsign = json.loads(get_content(sign_url))['playsign']

        #to be injected and replace ct10 and 12
        api85_url = 'http://play.youku.com/partner/get.json?cid={client_id}&vid={vid}&ct=85&sign={playsign}'.format(client_id = client_id, vid = vid, playsign = playsign)
        api86_url = 'http://play.youku.com/partner/get.json?cid={client_id}&vid={vid}&ct=86&sign={playsign}'.format(client_id = client_id, vid = vid, playsign = playsign)

        self.prepare(api_url = api85_url, api12_url = api86_url, ctype = 86, **kwargs)

        #exact copy from original VideoExtractor
        if 'extractor_proxy' in kwargs and kwargs['extractor_proxy']:
            unset_proxy()

        try:
            self.streams_sorted = [dict([('id', stream_type['id'])] + list(self.streams[stream_type['id']].items())) for stream_type in self.__class__.stream_types if stream_type['id'] in self.streams]
        except:
            self.streams_sorted = [dict([('itag', stream_type['itag'])] + list(self.streams[stream_type['itag']].items())) for stream_type in self.__class__.stream_types if stream_type['itag'] in self.streams]

        self.extract(**kwargs)

        self.download(**kwargs)

site = Youku()
download = site.download_by_url
download_playlist = site.download_playlist_by_url

youku_download_by_vid = site.download_by_vid
youku_open_download_by_vid = site.open_download_by_vid
# Used by: acfun.py bilibili.py miomio.py tudou.py
