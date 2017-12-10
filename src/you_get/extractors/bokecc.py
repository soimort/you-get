#!/usr/bin/env python

from ..common import *
from ..extractor import VideoExtractor
import xml.etree.ElementTree as ET

class BokeCC(VideoExtractor):
    name = "BokeCC"

    stream_types = [  # we do now know for now, as we have to check the
                      # output from the API
    ]

    API_ENDPOINT = 'http://p.bokecc.com/'


    def download_by_id(self, vid = '', title = None, output_dir='.', merge=True, info_only=False,**kwargs):
        """self, str->None
        
        Keyword arguments:
        self: self
        vid: The video ID for BokeCC cloud, something like
        FE3BB999594978049C33DC5901307461
        
        Calls the prepare() to download the video.
        
        If no title is provided, this method shall try to find a proper title
        with the information providin within the
        returned content of the API."""

        assert vid

        self.prepare(vid = vid, title = title, **kwargs)

        self.extract(**kwargs)

        self.download(output_dir = output_dir, 
                    merge = merge, 
                    info_only = info_only, **kwargs)

    def prepare(self, vid = '', title = None, **kwargs):
        assert vid

        api_url = self.API_ENDPOINT + \
            'servlet/playinfo?vid={vid}&m=0'.format(vid = vid)  #return XML

        html = get_content(api_url)
        self.tree = ET.ElementTree(ET.fromstring(html))

        if self.tree.find('result').text != '1':
            log.wtf('API result says failed!')
            raise 

        if title is None:
            self.title = '_'.join([i.text for i in self.tree.iterfind('video/videomarks/videomark/markdesc')])
        else:
            self.title = title

        if not title:
            self.title = vid

        for i in self.tree.iterfind('video/quality'):
            quality = i.attrib ['value']
            url = i[0].attrib['playurl']
            self.stream_types.append({'id': quality,
                                      'video_profile': i.attrib ['desp']})
            self.streams[quality] = {'url': url,
                                     'video_profile': i.attrib ['desp']}
            self.streams_sorted = [dict([('id', stream_type['id'])] + list(self.streams[stream_type['id']].items())) for stream_type in self.__class__.stream_types if stream_type['id'] in self.streams]


    def extract(self, **kwargs):
        for i in self.streams:
            s = self.streams[i]
            _, s['container'], s['size'] = url_info(s['url'])
            s['src'] = [s['url']]
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
            _, s['container'], s['size'] = url_info(s['url'])
            s['src'] = [s['url']]

site = BokeCC()

# I don't know how to call the player directly so I just put it here
# just in case anyone touchs it -- Beining@Aug.24.2016
#download = site.download_by_url
#download_playlist = site.download_by_url

bokecc_download_by_id = site.download_by_id
