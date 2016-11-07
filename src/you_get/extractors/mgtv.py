#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..common import *
from ..extractor import VideoExtractor

from json import loads
from urllib.parse import urlsplit
from os.path import dirname
import re

class MGTV(VideoExtractor):
    name = "芒果 (MGTV)"

    # Last updated: 2015-11-24
    stream_types = [
        {'id': 'hd', 'container': 'flv', 'video_profile': '超清'},
        {'id': 'sd', 'container': 'flv', 'video_profile': '高清'},
        {'id': 'ld', 'container': 'flv', 'video_profile': '标清'},
    ]
    
    id_dic = {i['video_profile']:(i['id']) for i in stream_types}
    
    api_endpoint = 'http://v.api.mgtv.com/player/video?video_id={video_id}'

    @staticmethod
    def get_vid_from_url(url):
        """Extracts video ID from URL.
        """
        return match1(url, 'http://www.mgtv.com/v/\d/\d+/\w+/(\d+).html')
    
    #----------------------------------------------------------------------
    @staticmethod
    def get_mgtv_real_url(url):
        """str->list of str
        Give you the real URLs."""
        content = loads(get_content(url))
        m3u_url = content['info']
        split = urlsplit(m3u_url)
        
        base_url = "{scheme}://{netloc}{path}/".format(scheme = split[0],
                                                      netloc = split[1],
                                                      path = dirname(split[2]))

        content = get_content(content['info'])  #get the REAL M3U url, maybe to be changed later?
        segment_list = []
        for i in content.split():
            if not i.startswith('#'):  #not the best way, better we use the m3u8 package
                segment_list.append(base_url + i)
        return segment_list

    def download_playlist_by_url(self, url, **kwargs):
        pass

    def prepare(self, **kwargs):
        if self.url:
            self.vid = self.get_vid_from_url(self.url)
        content = get_content(self.api_endpoint.format(video_id = self.vid))
        content = loads(content)
        self.title = content['data']['info']['title']
        
        #stream_avalable = [i['name'] for i in content['data']['stream']]
        stream_available = {}
        for i in content['data']['stream']:
            stream_available[i['name']] = i['url']

        for s in self.stream_types:
            if s['video_profile'] in stream_available.keys():
                quality_id = self.id_dic[s['video_profile']]
                url = stream_available[s['video_profile']]
                url = re.sub( r'(\&arange\=\d+)', '', url)  #Un-Hum
                segment_list_this = self.get_mgtv_real_url(url)
                
                container_this_stream = ''
                size_this_stream = 0
                stream_fileid_list = []
                for i in segment_list_this:
                    _, container_this_stream, size_this_seg = url_info(i)
                    size_this_stream += size_this_seg
                    stream_fileid_list.append(os.path.basename(i).split('.')[0])
                    
            #make pieces
            pieces = []
            for i in zip(stream_fileid_list, segment_list_this):
                pieces.append({'fileid': i[0], 'segs': i[1],})

                self.streams[quality_id] = {
                        'container': 'flv',
                        'video_profile': s['video_profile'],
                        'size': size_this_stream,
                        'pieces': pieces
                    }
                
            if not kwargs['info_only']:
                self.streams[quality_id]['src'] = segment_list_this

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

site = MGTV()
download = site.download_by_url
download_playlist = site.download_playlist_by_url