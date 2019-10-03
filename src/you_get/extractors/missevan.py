"""
MIT License

Copyright (c) 2019 WaferJay

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import json
import os
import re

from ..common import get_content, urls_size, log
from ..extractor import VideoExtractor


class _NoMatchException(Exception):
    pass


class _Dispatcher(object):

    def __init__(self):
        self.entry = []

    def register(self, patterns, fun):
        if not isinstance(patterns, (list, tuple)):
            patterns = [patterns]

        patterns = [re.compile(reg) for reg in patterns]
        self.entry.append((patterns, fun))

    def endpoint(self, *patterns):
        assert patterns, 'patterns must not be empty'
        def _wrap(fun):
            self.register(patterns, fun)
            return fun
        return _wrap

    def test(self, url):
        return any(pa.search(url) for pas, _ in self.entry for pa in pas)

    def dispatch(self, url, *args, **kwargs):

        for patterns, fun in self.entry:

            for pa in patterns:

                match = pa.search(url)
                if not match:
                    continue

                kwargs.update(match.groupdict())
                return fun(*args, **kwargs)

        raise _NoMatchException()


missevan_stream_types = [
    {'id': '128bit', 'url_json_key': 'soundurl_128', 'desc': '128 Kbps'},
    {'id': '64bit', 'url_json_key': 'soundurl_64', 'desc': '64 Kbps'},
    {'id': '32bit', 'url_json_key': 'soundurl_32', 'desc': '32 Kbps'},
    {'id': 'covers', 'url_json_key': 'cover_image', 'desc': '封面图'},
    {'id': 'coversmini', 'url_json_key': 'cover_image', 'desc': '封面缩略图'}
]

def is_covers_stream(stream):
    stream = stream or ''
    return stream.lower() in ('covers', 'coversmini')

def get_file_extension(file_path, default=''):
    _, suffix = os.path.splitext(file_path)
    if suffix:
        # remove dot
        suffix = suffix[1:]
    return suffix or default


class MissEvanWithStream(VideoExtractor):

    name = 'MissEvan'
    stream_types = missevan_stream_types

    @classmethod
    def create(cls, title, streams, *, streams_sorted=None):
        obj = cls()
        obj.title = title
        obj.streams.update(streams)
        streams_sorted = streams_sorted or cls._setup_streams_sorted(streams)
        obj.streams_sorted.extend(streams_sorted)
        return obj

    def fetch_danmaku(self, url, headers=None):
        self.danmaku = get_content(url, headers or {})
        return self

    @staticmethod
    def _setup_streams_sorted(streams):
        streams_sorted = []
        for key, stream in streams.items():
            copy_stream = stream.copy()
            copy_stream['id'] = key
            streams_sorted.append(copy_stream)

        return streams_sorted

    def download(self, **kwargs):
        stream_id = kwargs.get('stream_id') or self.stream_types[0]['id']
        stream = self.streams[stream_id]
        if 'size' not in stream:
            stream['size'] = urls_size(stream['src'])

        super().download(**kwargs)

    def unsupported_method(self, *args, **kwargs):
        raise AssertionError('Unsupported')

    download_by_url = unsupported_method
    download_by_vid = unsupported_method
    prepare = unsupported_method
    extract = unsupported_method


class MissEvan(VideoExtractor):

    name = 'MissEvan'
    stream_types = missevan_stream_types

    __prepare_dispatcher = _Dispatcher()

    @__prepare_dispatcher.endpoint(
        re.compile(r'missevan\.com/sound/(?:player\?.*?id=)?(?P<sid>\d+)', re.I))
    def prepare_sound(self, sid, **kwargs):
        content = get_content(self.url_sound_api(sid))
        json_data = json.loads(content)
        sound = json_data['info']['sound']

        self.title = sound['soundstr']
        if not is_covers_stream(kwargs.get('stream_id')):
            self.danmaku = get_content(self.url_danmaku_api(sid))

        self.streams = self.setup_streams(sound)

    @classmethod
    def setup_streams(cls, sound):
        streams = {}

        for stream_type in cls.stream_types:
            stream_id = stream_type['id']
            uri = sound[stream_type['url_json_key']]
            if is_covers_stream(stream_id):
                resource_url = cls.url_resource(stream_id + '/' + uri)
            else:
                resource_url = cls.url_resource(uri)

            container = get_file_extension(uri)
            streams[stream_id] = {'src': [resource_url], 'container': container}
        return streams

    def prepare(self, **kwargs):
        if self.vid:
            self.prepare_sound(self.vid, **kwargs)
            return

        try:
            self.__prepare_dispatcher.dispatch(self.url, self, **kwargs)
        except _NoMatchException:
            log.e('[Error] Unsupported URL pattern.')
            exit(1)

    @staticmethod
    def download_covers(title, streams, **kwargs):
        if not is_covers_stream(kwargs.get('stream_id')):
            kwargs['stream_id'] = 'covers'
            MissEvanWithStream \
                .create(title, streams) \
                .download(**kwargs)

    _download_playlist_dispatcher = _Dispatcher()

    @_download_playlist_dispatcher.endpoint(
        re.compile(r'missevan\.com/album(?:info)?/(?P<aid>\d+)', re.I))
    def download_album(self, aid, **kwargs):
        content = get_content(self.url_album_api(aid))
        json_data = json.loads(content)
        album = json_data['info']['album']
        self.title = album['title']
        sounds = json_data['info']['sounds']

        output_dir = os.path.abspath(kwargs.pop('output_dir', '.'))
        output_dir = os.path.join(output_dir, self.title)
        kwargs['output_dir'] = output_dir

        for sound in sounds:
            streams = self.setup_streams(sound)
            sound_id = sound['id']
            sound_title = sound['soundstr']
            MissEvanWithStream \
                .create(sound_title, streams) \
                .fetch_danmaku(self.url_danmaku_api(sound_id)) \
                .download(**kwargs)

            self.download_covers(sound_title, streams, **kwargs)

    @_download_playlist_dispatcher.endpoint(
        re.compile(r'missevan\.com(?:/mdrama)?/drama/(?P<did>\d+)', re.I))
    def download_drama(self, did, **kwargs):
        content = get_content(self.url_drama_api(did))
        json_data = json.loads(content)

        drama = json_data['info']['drama']

        self.title = drama['name']
        output_dir = os.path.abspath(kwargs.pop('output_dir', '.'))
        output_dir = os.path.join(output_dir, self.title)
        kwargs['output_dir'] = output_dir

        episodes = json_data['info']['episodes']
        for each in episodes['episode']:
            sound_id = each['sound_id']
            MissEvan().download_by_vid(sound_id, **kwargs)

    def download_playlist_by_url(self, url, **kwargs):
        # use the best quality by default
        kwargs.setdefault('stream_id', self.stream_types[0]['id'])

        self.url = url
        try:
            self._download_playlist_dispatcher.dispatch(url, self, **kwargs)
        except _NoMatchException:
            log.e('[Error] Unsupported URL pattern with --playlist option.')
            exit(1)

    def download_by_url(self, url, **kwargs):
        if not kwargs.get('playlist') and self._download_playlist_dispatcher.test(url):
            log.w('This is an album or drama. (use --playlist option to download all).')
        else:
            super().download_by_url(url, **kwargs)

    def download(self, **kwargs):
        kwargs['keep_obj'] = True   # keep the self.streams to download covers
        super().download(**kwargs)
        self.download_covers(self.title, self.streams, **kwargs)

    def extract(self, **kwargs):
        stream_id = kwargs.get('stream_id') or self.stream_types[0]['id']
        stream = self.streams[stream_id]
        if 'size' not in stream:
            stream['size'] = urls_size(stream['src'])

    @staticmethod
    def url_album_api(album_id):
        return 'https://www.missevan.com/sound/soundalllist?albumid=' + str(album_id)

    @staticmethod
    def url_sound_api(sound_id):
        return 'https://www.missevan.com/sound/getsound?soundid=' + str(sound_id)

    @staticmethod
    def url_drama_api(drama_id):
        return 'https://www.missevan.com/dramaapi/getdrama?drama_id=' + str(drama_id)

    @staticmethod
    def url_danmaku_api(sound_id):
        return 'https://www.missevan.com/sound/getdm?soundid=' + str(sound_id)

    @staticmethod
    def url_resource(uri):
        return 'https://static.missevan.com/' + uri

site = MissEvan()
site_info = 'MissEvan.com'
download = site.download_by_url
download_playlist = site.download_playlist_by_url
