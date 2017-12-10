#!/usr/bin/env python

from ..common import *
from ..extractor import VideoExtractor

import ssl

class Infoq(VideoExtractor):
    name = "InfoQ"

    stream_types = [
        {'id': 'video'},
        {'id': 'audio'},
        {'id': 'slides'}
    ]

    def prepare(self, **kwargs):
        content = get_content(self.url)
        self.title = match1(content, r'<title>([^<]+)</title>')
        s = match1(content, r'P\.s\s*=\s*\'([^\']+)\'')
        scp = match1(content, r'InfoQConstants\.scp\s*=\s*\'([^\']+)\'')
        scs = match1(content, r'InfoQConstants\.scs\s*=\s*\'([^\']+)\'')
        sck = match1(content, r'InfoQConstants\.sck\s*=\s*\'([^\']+)\'')

        mp3 = match1(content, r'name="filename"\s*value="([^"]+\.mp3)"')
        if mp3: mp3 = 'http://res.infoq.com/downloads/mp3downloads/%s' % mp3

        pdf = match1(content, r'name="filename"\s*value="([^"]+\.pdf)"')
        if pdf: pdf = 'http://res.infoq.com/downloads/pdfdownloads/%s' % pdf

        # cookie handler
        ssl_context = request.HTTPSHandler(
            context=ssl.SSLContext(ssl.PROTOCOL_TLSv1))
        cookie_handler = request.HTTPCookieProcessor()
        opener = request.build_opener(ssl_context, cookie_handler)
        opener.addheaders = [
            ('Referer', self.url),
            ('Cookie',
             'CloudFront-Policy=%s;CloudFront-Signature=%s;CloudFront-Key-Pair-Id=%s' % (scp, scs, sck))
        ]
        request.install_opener(opener)

        if s: self.streams['video'] = {'url': s }
        if mp3: self.streams['audio'] = { 'url': mp3 }
        if pdf: self.streams['slides'] = { 'url': pdf }

    def extract(self, **kwargs):
        for i in self.streams:
            s = self.streams[i]
            _, s['container'], s['size'] = url_info(s['url'])
            s['src'] = [s['url']]

site = Infoq()
download = site.download_by_url
download_playlist = site.download_by_url
