#!/usr/bin/env python
import base64

import binascii

from ..common import *
import random
import string
import ctypes
from json import loads
from urllib import request

__all__ = ['ixigua_download', 'ixigua_download_playlist_by_url']

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 "
                  "Safari/537.36",
}


def ixigua_download(url, output_dir='.', merge=True, info_only=False, stream_id='', **kwargs):
    # example url: https://www.ixigua.com/i6631065141750268420/#mid=63024814422
    headers['cookie'] = "MONITOR_WEB_ID=7892c49b-296e-4499-8704-e47c1b15123; " \
                        "ixigua-a-s=1; ttcid=af99669b6304453480454f1507011d5c234; BD_REF=1; " \
                        "__ac_nonce=060d88ff000a75e8d17eb; __ac_signature=_02B4Z6wo100f01kX9ZpgAAIDAKIBBQUIPYT5F2WIAAPG2ad; " \
                        "ttwid=1%7CcIsVF_3vqSIk4XErhPB0H2VaTxT0tdsTMRbMjrJOPN8%7C1624806049%7C08ce7dd6f7d20506a41ba0a331ef96a6505d96731e6ad9f6c8c709f53f227ab1; "

    resp = urlopen_with_retry(request.Request(url, headers=headers))
    html = resp.read().decode('utf-8')

    _cookies = []
    for c in resp.getheader('Set-Cookie').split("httponly,"):
        _cookies.append(c.strip().split(' ')[0])
    headers['cookie'] += ' '.join(_cookies)

    match_txt = match1(html, r"<script id=\"SSR_HYDRATED_DATA\">window._SSR_HYDRATED_DATA=(.*?)<\/script>")
    if not match_txt:
        log.e("Get video info from url failed, url: {}".format(url))
        return
    video_info = loads(match_txt.replace('":undefined', '":null'))
    if not video_info:
        log.e("video_info not found, url:{}".format(url))
        return

    title = video_info['anyVideo']['gidInformation']['packerData']['video']['title']
    video_resource = video_info['anyVideo']['gidInformation']['packerData']['video']['videoResource']
    if video_resource.get('dash', None):
        video_list = video_resource['dash']
    elif video_resource.get('dash_120fps', None):
        video_list = video_resource['dash_120fps']
    elif video_resource.get('normal', None):
        video_list = video_resource['normal']
    else:
        log.e("video_list not found, url:{}".format(url))
        return

    streams = [
        # {'file_id': 'fc1b9bf8e8e04a849d90a5172d3f6919', 'quality': "normal", 'size': 0,
        #  'definition': '720p', 'video_url': '','audio_url':'','v_type':'dash'},
    ]
    # 先用无水印的视频与音频合成，没有的话，再直接用有水印的mp4
    if video_list.get('dynamic_video', None):
        audio_url = base64.b64decode(
            video_list['dynamic_video']['dynamic_audio_list'][0]['main_url'].encode("utf-8")).decode("utf-8")
        dynamic_video_list = video_list['dynamic_video']['dynamic_video_list']
        streams = convertStreams(dynamic_video_list, audio_url)
    elif video_list.get('video_list', None):
        dynamic_video_list = video_list['video_list']
        streams = convertStreams(dynamic_video_list, "")

    print("title:          %s" % title)
    for stream in streams:
        if stream_id != "" and stream_id != stream['definition']:
            continue

        print("    - format:        %s" % stream['definition'])
        print("      size:          %s MiB (%s bytes)" % (round(stream['size'] / 1048576, 1), stream['size']))
        print("      quality:       %s " % stream['quality'])
        print("      v_type:        %s " % stream['v_type'])
        # print("      video_url:          %s " % stream['video_url'])
        # print("      audio_url:          %s " % stream['audio_url'])
        print()

        # 不是只看信息的话，就下载第一个
        if not info_only:
            urls = [stream['video_url']]
            if stream['audio_url'] != "":
                urls.append(stream['audio_url'])
                kwargs['av'] = 'av'  # 这将会合并音视频

            download_urls(urls, title, "mp4", stream['size'], output_dir, merge=merge, headers=headers,
                          **kwargs)
            return


def convertStreams(video_list, audio_url):
    streams = []
    if type(video_list) == dict:
        video_list = video_list.values()
    for dynamic_video in video_list:
        streams.append({
            'file_id': dynamic_video['file_hash'],
            'quality': dynamic_video['quality'],
            'size': dynamic_video['size'],
            'definition': dynamic_video['definition'],
            'video_url': base64.b64decode(dynamic_video['main_url'].encode("utf-8")).decode("utf-8"),
            'audio_url': audio_url,
            'v_type': dynamic_video['vtype'],
        })

    return streams


def ixigua_download_playlist_by_url(url, output_dir='.', merge=True, info_only=False, **kwargs):
    assert "user" in url, "Only support users to publish video list,Please provide a similar url:" \
                          "https://www.ixigua.com/c/user/6907091136/"

    user_id = url.split("/")[-2] if url[-1] == "/" else url.split("/")[-1]
    params = {"max_behot_time": "0", "max_repin_time": "0", "count": "20", "page_type": "0", "user_id": user_id}
    while 1:
        url = "https://www.ixigua.com/c/user/article/?" + "&".join(["{}={}".format(k, v) for k, v in params.items()])
        video_list = loads(get_content(url, headers=headers))
        params["max_behot_time"] = video_list["next"]["max_behot_time"]
        for video in video_list["data"]:
            ixigua_download("https://www.ixigua.com/i{}/".format(video["item_id"]), output_dir, merge, info_only,
                            **kwargs)
        if video_list["next"]["max_behot_time"] == 0:
            break


site_info = "ixigua.com"
download = ixigua_download
download_playlist = ixigua_download_playlist_by_url
