#!/usr/bin/env python

from ..common import *
from ..extractor import VideoExtractor

import json

class Bigthink(VideoExtractor):
    name = "Bigthink"

    stream_types = [  #this is just a sample. Will make it in prepare()
        # {'id': '1080'},
        # {'id': '720'},
        # {'id': '360'},
        # {'id': '288'},
        # {'id': '190'},
        # {'id': '180'},
        
    ]

    @staticmethod
    def get_streams_by_id(account_number, video_id):
        """
        int, int->list
        
        Get the height of the videos.
        
        Since brightcove is using 3 kinds of links: rtmp, http and https,
        we will be using the HTTPS one to make it secure.
        
        If somehow akamaihd.net is blocked by the Great Fucking Wall,
        change the "startswith https" to http.
        """
        endpoint = 'https://edge.api.brightcove.com/playback/v1/accounts/{account_number}/videos/{video_id}'.format(account_number = account_number, video_id = video_id)
        fake_header_id = fake_headers
        #is this somehow related to the time? Magic....
        fake_header_id['Accept'] ='application/json;pk=BCpkADawqM1cc6wmJQC2tvoXZt4mrB7bFfi6zGt9QnOzprPZcGLE9OMGJwspQwKfuFYuCjAAJ53JdjI8zGFx1ll4rxhYJ255AXH1BQ10rnm34weknpfG-sippyQ'

        html = get_content(endpoint, headers= fake_header_id)
        html_json = json.loads(html)

        link_list = []

        for i in html_json['sources']:
            if 'src' in i:  #to avoid KeyError
                if i['src'].startswith('https'):
                    link_list.append((str(i['height']), i['src']))

        return link_list

    def prepare(self, **kwargs):

        html = get_content(self.url)

        self.title = match1(html, r'<meta property="og:title" content="([^"]*)"')

        account_number = match1(html, r'data-account="(\d+)"')

        video_id = match1(html, r'data-brightcove-id="(\d+)"')
        
        assert account_number, video_id

        link_list = self.get_streams_by_id(account_number, video_id)

        for i in link_list:
            self.stream_types.append({'id': str(i[0])})
            self.streams[i[0]] = {'url': i[1]}

    def extract(self, **kwargs):
        for i in self.streams:
            s = self.streams[i]
            _, s['container'], s['size'] = url_info(s['url'])
            s['src'] = [s['url']]

site = Bigthink()
download = site.download_by_url
