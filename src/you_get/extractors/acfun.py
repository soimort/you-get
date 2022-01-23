#!/usr/bin/env python

from ..common import *
from ..extractor import VideoExtractor

class AcFun(VideoExtractor):
    name = "AcFun"

    stream_types = [
        {'id': '2160P', 'qualityType': '2160p'},
        {'id': '1080P60', 'qualityType': '1080p60'},
        {'id': '720P60', 'qualityType': '720p60'},
        {'id': '1080P+', 'qualityType': '1080p+'},
        {'id': '1080P', 'qualityType': '1080p'},
        {'id': '720P', 'qualityType': '720p'},
        {'id': '540P', 'qualityType': '540p'},
        {'id': '360P', 'qualityType': '360p'}
    ]    

    def prepare(self, **kwargs):
        assert re.match(r'https?://[^\.]*\.*acfun\.[^\.]+/(\D|bangumi)/\D\D(\d+)', self.url)

        if re.match(r'https?://[^\.]*\.*acfun\.[^\.]+/\D/\D\D(\d+)', self.url):
            html = get_content(self.url, headers=fake_headers)
            json_text = match1(html, r"(?s)videoInfo\s*=\s*(\{.*?\});")
            json_data = json.loads(json_text)
            vid = json_data.get('currentVideoInfo').get('id')
            up = json_data.get('user').get('name')
            self.title = json_data.get('title')
            video_list = json_data.get('videoList')
            if len(video_list) > 1:
                self.title += " - " + [p.get('title') for p in video_list if p.get('id') == vid][0]
            currentVideoInfo = json_data.get('currentVideoInfo')

        elif re.match("https?://[^\.]*\.*acfun\.[^\.]+/bangumi/aa(\d+)", self.url):
            html = get_content(self.url, headers=fake_headers)
            tag_script = match1(html, r'<script>\s*window\.pageInfo([^<]+)</script>')
            json_text = tag_script[tag_script.find('{') : tag_script.find('};') + 1]
            json_data = json.loads(json_text)
            self.title = json_data['bangumiTitle'] + " " + json_data['episodeName'] + " " + json_data['title']
            vid = str(json_data['videoId'])
            up = "acfun"
            currentVideoInfo = json_data.get('currentVideoInfo')

        else:
            raise NotImplemented            

        if 'ksPlayJson' in currentVideoInfo:
            durationMillis = currentVideoInfo['durationMillis']
            ksPlayJson = ksPlayJson = json.loads( currentVideoInfo['ksPlayJson'] )
            representation = ksPlayJson.get('adaptationSet')[0].get('representation')
            stream_list = representation

        for stream in stream_list:
            m3u8_url = stream["url"]
            size = durationMillis * stream["avgBitrate"] / 8
            # size = float('inf')
            container = 'mp4'
            stream_id = stream["qualityLabel"]
            quality = stream["qualityType"]
            
            stream_data = dict(src=m3u8_url, size=size, container=container, quality=quality)
            self.streams[stream_id] = stream_data

        assert self.title and m3u8_url
        self.title = unescape_html(self.title)
        self.title = escape_file_path(self.title)
        p_title = r1('active">([^<]+)', html)
        self.title = '%s (%s)' % (self.title, up)
        if p_title:
            self.title = '%s - %s' % (self.title, p_title)       


    def download(self, **kwargs):
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
                stream_id = self.streams_sorted[0]['id'] if 'id' in self.streams_sorted[0] else self.streams_sorted[0]['itag']

            if 'index' not in kwargs:
                self.p(stream_id)
            else:
                self.p_i(stream_id)
            if stream_id in self.streams:
                url = self.streams[stream_id]['src']
                ext = self.streams[stream_id]['container']
                total_size = self.streams[stream_id]['size']


            if ext == 'm3u8' or ext == 'm4a':
                ext = 'mp4'

            if not url:
                log.wtf('[Failed] Cannot extract video source.')
            # For legacy main()
            headers = {}
            if self.ua is not None:
                headers['User-Agent'] = self.ua
            if self.referer is not None:
                headers['Referer'] = self.referer

            download_url_ffmpeg(url, self.title, ext, output_dir=kwargs['output_dir'], merge=kwargs['merge'])                           

            if 'caption' not in kwargs or not kwargs['caption']:
                print('Skipping captions or danmaku.')
                return

            for lang in self.caption_tracks:
                filename = '%s.%s.srt' % (get_filename(self.title), lang)
                print('Saving %s ... ' % filename, end="", flush=True)
                srt = self.caption_tracks[lang]
                with open(os.path.join(kwargs['output_dir'], filename),
                          'w', encoding='utf-8') as x:
                    x.write(srt)
                print('Done.')

            if self.danmaku is not None and not dry_run:
                filename = '{}.cmt.xml'.format(get_filename(self.title))
                print('Downloading {} ...\n'.format(filename))
                with open(os.path.join(kwargs['output_dir'], filename), 'w', encoding='utf8') as fp:
                    fp.write(self.danmaku)

            if self.lyrics is not None and not dry_run:
                filename = '{}.lrc'.format(get_filename(self.title))
                print('Downloading {} ...\n'.format(filename))
                with open(os.path.join(kwargs['output_dir'], filename), 'w', encoding='utf8') as fp:
                    fp.write(self.lyrics)

            # For main_dev()
            #download_urls(urls, self.title, self.streams[stream_id]['container'], self.streams[stream_id]['size'])
        keep_obj = kwargs.get('keep_obj', False)
        if not keep_obj:
            self.__init__()


    def acfun_download(self, url, output_dir='.', merge=True, info_only=False, **kwargs):
        assert re.match(r'https?://[^\.]*\.*acfun\.[^\.]+/(\D|bangumi)/\D\D(\d+)', url)

        def getM3u8UrlFromCurrentVideoInfo(currentVideoInfo):
            if 'playInfos' in currentVideoInfo:
                return currentVideoInfo['playInfos'][0]['playUrls'][0]
            elif 'ksPlayJson' in currentVideoInfo:
                ksPlayJson = json.loads( currentVideoInfo['ksPlayJson'] )
                representation = ksPlayJson.get('adaptationSet')[0].get('representation')
                reps = []
                for one in representation:
                    reps.append( (one['width']* one['height'], one['url'], one['backupUrl']) )
                return max(reps)[1]


        if re.match(r'https?://[^\.]*\.*acfun\.[^\.]+/\D/\D\D(\d+)', url):
            html = get_content(url, headers=fake_headers)
            json_text = match1(html, r"(?s)videoInfo\s*=\s*(\{.*?\});")
            json_data = json.loads(json_text)
            vid = json_data.get('currentVideoInfo').get('id')
            up = json_data.get('user').get('name')
            title = json_data.get('title')
            video_list = json_data.get('videoList')
            if len(video_list) > 1:
                title += " - " + [p.get('title') for p in video_list if p.get('id') == vid][0]
            currentVideoInfo = json_data.get('currentVideoInfo')
            m3u8_url = getM3u8UrlFromCurrentVideoInfo(currentVideoInfo)
        elif re.match("https?://[^\.]*\.*acfun\.[^\.]+/bangumi/aa(\d+)", url):
            html = get_content(url, headers=fake_headers)
            tag_script = match1(html, r'<script>\s*window\.pageInfo([^<]+)</script>')
            json_text = tag_script[tag_script.find('{') : tag_script.find('};') + 1]
            json_data = json.loads(json_text)
            title = json_data['bangumiTitle'] + " " + json_data['episodeName'] + " " + json_data['title']
            vid = str(json_data['videoId'])
            up = "acfun"

            currentVideoInfo = json_data.get('currentVideoInfo')
            m3u8_url = getM3u8UrlFromCurrentVideoInfo(currentVideoInfo)

        else:
            raise NotImplemented

        assert title and m3u8_url
        title = unescape_html(title)
        title = escape_file_path(title)
        p_title = r1('active">([^<]+)', html)
        title = '%s (%s)' % (title, up)
        if p_title:
            title = '%s - %s' % (title, p_title)

        print_info(site_info, title, 'm3u8', float('inf'))
        if not info_only:
            download_url_ffmpeg(m3u8_url, title, 'mp4', output_dir=output_dir, merge=merge)

site = AcFun()
site_info = "AcFun.cn"
download = site.download_by_url
download_playlist = playlist_not_supported('acfun')
