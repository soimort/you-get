#!/usr/bin/env python
__all__ = ['iwara_download']
from ..common import *
headers = {
    'DNT': '1',
    'Accept-Encoding': 'gzip, deflate, sdch, br',
    'Accept-Language': 'en-CA,en;q=0.8,en-US;q=0.6,zh-CN;q=0.4,zh;q=0.2',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.75 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Save-Data': 'on',
    'Cookie':'has_js=1;show_adult=1',
}
stream_types = [
        {'id': 'Source',      'container': 'mp4', 'video_profile': '原始'},
        {'id': '540p',    'container': 'mp4', 'video_profile': '540p'},
        {'id': '360p',   'container': 'mp4', 'video_profile': '360P'},
    ]
def iwara_download(url, output_dir='.', merge=True, info_only=False, **kwargs):
    global headers
    video_hash = match1(url, r'https?://\w+.iwara.tv/videos/(\w+)')
    video_url = match1(url, r'(https?://\w+.iwara.tv)/videos/\w+')
    html = get_content(url, headers=headers)
    title = r1(r'<title>(.*)</title>', html)
    api_url = video_url + '/api/video/' + video_hash
    content = get_content(api_url, headers=headers)
    data = json.loads(content)
    down_urls = 'https:' + data[0]['uri']
    type, ext, size = url_info(down_urls, headers=headers)
    print_info(site_info, title+data[0]['resolution'], type, size)

    if not info_only:
        download_urls([down_urls], title, ext, size, output_dir, merge=merge, headers=headers)

def download_playlist_by_url( url, **kwargs):
    video_page = get_content(url)
    # url_first=re.findall(r"(http[s]?://[^/]+)",url)
    url_first=match1(url, r"(http[s]?://[^/]+)")
    # print (url_first)
    videos = set(re.findall(r'<a href="(/videos/[^"]+)"', video_page))
    if(len(videos)>0):
        for video in videos:
            iwara_download(url_first+video, **kwargs)
    else:
        maybe_print('this page not found any videos')
site_info = "Iwara"
download = iwara_download
download_playlist = download_playlist_by_url
