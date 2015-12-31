#!/usr/bin/env python

from ..common import *
from ..extractor import VideoExtractor

import ssl

class Videomega(VideoExtractor):
    name = "Videomega"

    stream_types = [
        {'id': 'original'}
    ]

    def prepare(self, **kwargs):
        # Hot-plug cookie handler
        ssl_context = request.HTTPSHandler(
            context=ssl.SSLContext(ssl.PROTOCOL_TLSv1))
        cookie_handler = request.HTTPCookieProcessor()
        opener = request.build_opener(ssl_context, cookie_handler)
        opener.addheaders = [('Referer', self.url),
                             ('Cookie', 'noadvtday=0')]
        request.install_opener(opener)

        ref = match1(self.url, r'ref=(\w+)')
        php_url = 'http://videomega.tv/view.php?ref=' + ref
        content = get_content(php_url)

        self.title = match1(content, r'<title>(.*)</title>')
        js = match1(content, r'(eval.*)')
        t = match1(js, r'\$\("\d+"\)\.\d+\("\d+","([^"]+)"\)')
        t = re.sub(r'(\w)', r'{\1}', t)
        t = t.translate({87 + i: str(i) for i in range(10, 36)})
        s = match1(js, r"'([^']+)'\.split").split('|')
        self.streams['original'] = {
            'url': t.format(*s)
        }

    def extract(self, **kwargs):
        for i in self.streams:
            s = self.streams[i]
            _, s['container'], s['size'] = url_info(s['url'])
            s['src'] = [s['url']]

site = Videomega()
download = site.download_by_url
download_playlist = site.download_by_url
