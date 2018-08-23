#!/usr/bin/env python

__all__ = ['songtasty_download']

from ..common import *
import urllib.error
from time import time
from urllib.parse import quote
from json import loads

def songtasty_download(url, output_dir = '.', merge=True, info_only=False, **kwargs):
    if re.match(r'http://www.songtasty.com/song/(\d)+', url):
        html = get_content(url)
        # example: <span id="play_musicname">不加糖先生° ▍ - 童年不能忘却的音乐 - 地球仪 电音版</span>
        title = r1(r'<title(.*)</title>', html)
        # <div id="audios" data-rel="http://newst.bailemi.com/20180822/GwKAYKwzCTzkmQQi86CPSneApmwbfMhM.mp3" class="bdsharebuttonbox">
        # example <audio id="jp_audio_0" preload="metadata" src="http://newst.bailemi.com/20180822/GwKAYKwzCTzkmQQi86CPSneApmwbfMhM.mp3"></audio>
        downloadurl = r1(r'<div id="audios" data-rel="(.*)" .*>', html)
        if not info_only:
            download_urls([downloadurl], title, 'MP3', total_size=0, output_dir = output_dir, merge = merge)
    else:
        log.wtf("Not support songtasty url, should be http://www.songtasty.com/song/12345", 1)
site_info = "songtasty"
download = songtasty_download
download_playlist = playlist_not_supported('songtasty')
