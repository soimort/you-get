#!/usr/bin/env python

from ..common import *
from ..extractor import VideoExtractor

class Spankbang(VideoExtractor):
    name = "Spankbang"
    
    # ordered list of supported stream types / qualities on this site
    # order: high quality -> low quality
    stream_types = [#there are at most 4 different streams
        {'id': '1080p', 'container': 'mp4', 'video_profile': 'super'},
        {'id': '720p', 'container': 'mp4', 'video_profile': 'high'},
        {'id': '480p', 'container': 'mp4', 'video_profile': 'medium'},
        {'id': '240p', 'container': 'mp4', 'video_profile': 'low'},        
    ]
    
    def prepare(self, **kwargs):
        kwargs['kwargs'] = True
        self.title = self.url.split('/')[-1]
        video_url_pattern = r'http://spankbang.com/_{stream_id}/' \
                            r'{stream_key}/title/{quality}'
        stream_quality = [('q_super','1080p__mp4','1080p'),
                          ('q_high','720p__mp4','720p'),
                          ('q_medium','480p__mp4','480p'),
                          ('q_low','240p__mp4','240p')]

        content = get_decoded_html(self.url, faker = True)
        stream_id = match1(content, r'stream_id.+?\'(.+)\'')
        stream_key = match1(content, r'stream_key.+?\'(.+)\'')
        for key, quality, itag in stream_quality:
            if content.find(key) != -1:
                video_url = video_url_pattern.format(stream_id=stream_id,
                                                     stream_key=stream_key,
                                                     quality=quality)
                self.streams[itag] = {'url': video_url}
    
    def extract(self, **kwargs):
        for i in self.streams:
            s = self.streams[i]
            _, s['container'], s['size'] = url_info(s['url'], faker = True)
            s['src'] = [s['url']]
            
    def download(self, **kwargs):
        # I just want to set faker=True in download_urls but have to override the whole method
        # anyone can make it less complicated?
        if 'json_output' in kwargs and kwargs['json_output']:
            json_output.output(self)
        elif 'info_only' in kwargs and kwargs['info_only']:
            if 'stream_id' in kwargs and kwargs['stream_id']:
                # Display the stream
                stream_id = kwargs['stream_id']
                if 'index' not in kwargs:
                    self.p(stream_id)
                else:
                    self.p_i(stream_id)
            else:
                # Display all available streams
                if 'index' not in kwargs:
                    self.p([])
                else:
                    stream_id = self.streams_sorted[0]['id'] if 'id' in self.streams_sorted[0] else self.streams_sorted[0]['itag']
                    self.p_i(stream_id)

        else:
            if 'stream_id' in kwargs and kwargs['stream_id']:
                # Download the stream
                stream_id = kwargs['stream_id']
            else:
                # Download stream with the best quality
                stream_id = self.streams_sorted[0]['id'] if 'id' in self.streams_sorted[0] else self.streams_sorted[0]['itag']

            if 'index' not in kwargs:
                self.p(stream_id)
            else:
                self.p_i(stream_id)

            if stream_id in self.streams:
                urls = self.streams[stream_id]['src']
                ext = self.streams[stream_id]['container']
                total_size = self.streams[stream_id]['size']
            else:
                urls = self.dash_streams[stream_id]['src']
                ext = self.dash_streams[stream_id]['container']
                total_size = self.dash_streams[stream_id]['size']

            if not urls:
                log.wtf('[Failed] Cannot extract video source.')
            # For legacy main()
            download_urls(urls, self.title, ext, total_size,
                          output_dir=kwargs['output_dir'],
                          merge=kwargs['merge'],
                          av=stream_id in self.dash_streams,
                          faker=True)
            if 'caption' not in kwargs or not kwargs['caption']:
                print('Skipping captions.')
                return
            for lang in self.caption_tracks:
                filename = '%s.%s.srt' % (get_filename(self.title), lang)
                print('Saving %s ... ' % filename, end="", flush=True)
                srt = self.caption_tracks[lang]
                with open(os.path.join(kwargs['output_dir'], filename),
                          'w', encoding='utf-8') as x:
                    x.write(srt)
                print('Done.')

            # For main_dev()
            #download_urls(urls, self.title, self.streams[stream_id]['container'], self.streams[stream_id]['size'])

        self.__init__()

site = Spankbang()
download = site.download_by_url
#todo: download_playlist
