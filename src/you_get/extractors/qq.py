#!/usr/bin/env python
# -*- coding: utf-8 -*-


from ..common import *
from ..extractor import VideoExtractor


class QQ(VideoExtractor):
    name = "腾讯 (QQ)"

    stream_types = [
        {'id': 'mp4', 'container': 'mp4', 'video_profile': '标清'},
    ]

    def get_prepare_data(url):
        content = get_html(url)
        vid = match1(content, r'vid\s*:\s*"\s*([^"]+)"')
        title = match1(content, r'title\s*:\s*"\s*([^"]+)"')

        return {'vid': vid, 'title': title}


    def prepare(self, **kwargs):
        assert self.url or self.vid

        if not self.vid:
            prepare_data = self.__class__.get_prepare_data(self.url)
            self.vid = prepare_data['vid']
            self.title = prepare_data['title']

        self.site = self.name

        api = "http://vv.video.qq.com/geturl?otype=json&vid=%s" % self.vid
        content = get_html(api)

        output_json = json.loads(match1(content, r'QZOutputJson=(.*)')[:-1])
        url = output_json['vd']['vi'][0]['url']
        _, ext, size = url_info(url, faker=True)

        stream_types = dict([(i['id'], i) for i in self.stream_types])
        stream_id = ext
        if stream_id in stream_types:
            self.streams[stream_id] = {
                'container': stream_types[stream_id]['container'],
                'video_profile': stream_types[stream_id]['video_profile'],
                'size': size,
                'src': [url],
            }

    def extract(self, **kwargs):
        pass


def qq_download_by_url(*args, **kwargs):
    site.download_by_url(*args, **kwargs)

def qq_download_by_vid(*args, **kwargs):
    site.title = args[1]
    site.download_by_vid(*args, **kwargs)

# def qq_download_by_vid(vid, title, output_dir='.', merge=True, info_only=False):
#     api = "http://vv.video.qq.com/geturl?otype=json&vid=%s" % vid
#     content = get_html(api)
#     output_json = json.loads(match1(content, r'QZOutputJson=(.*)')[:-1])
#     url = output_json['vd']['vi'][0]['url']
#     _, ext, size = url_info(url, faker=True)
#
#     print_info(site_info, title, ext, size)
#     if not info_only:
#         download_urls([url], title, ext, size, output_dir=output_dir, merge=merge)
#
# def qq_download(url, output_dir='.', merge=True, info_only=False, **kwargs):
#     content = get_html(url)
#     vid = match1(content, r'vid\s*:\s*"\s*([^"]+)"')
#     title = match1(content, r'title\s*:\s*"\s*([^"]+)"')
#
#     qq_download_by_vid(vid, title, output_dir, merge, info_only)

site_info = "QQ.com"
site = QQ()
download = qq_download_by_url
download_playlist = playlist_not_supported('qq')
