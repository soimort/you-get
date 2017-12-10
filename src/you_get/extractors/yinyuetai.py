#!/usr/bin/env python

__all__ = ['yinyuetai_download', 'yinyuetai_download_by_id']

from ..common import *

def yinyuetai_download_by_id(vid, title=None, output_dir='.', merge=True, info_only=False):
    video_info = json.loads(get_html('http://www.yinyuetai.com/insite/get-video-info?json=true&videoId=%s' % vid))
    url_models = video_info['videoInfo']['coreVideoInfo']['videoUrlModels']
    url_models = sorted(url_models, key=lambda i: i['qualityLevel'])
    url = url_models[-1]['videoUrl']
    type = ext = r1(r'\.(flv|mp4)', url)
    _, _, size = url_info(url)

    print_info(site_info, title, type, size)
    if not info_only:
        download_urls([url], title, ext, size, output_dir, merge = merge)

def yinyuetai_download(url, output_dir='.', merge=True, info_only=False, **kwargs):
    id = r1(r'http://\w+.yinyuetai.com/video/(\d+)', url) or \
         r1(r'http://\w+.yinyuetai.com/video/h5/(\d+)', url)
    if not id:
        yinyuetai_download_playlist(url, output_dir=output_dir, merge=merge, info_only=info_only)
        return

    html = get_html(url, 'utf-8')
    title = r1(r'<meta property="og:title"\s+content="([^"]+)"/>', html) or r1(r'<title>(.*)', html)
    assert title
    title = parse.unquote(title)
    title = escape_file_path(title)
    yinyuetai_download_by_id(id, title, output_dir, merge=merge, info_only=info_only)

def yinyuetai_download_playlist(url, output_dir='.', merge=True, info_only=False, **kwargs):
    playlist = r1(r'http://\w+.yinyuetai.com/playlist/(\d+)', url)
    html = get_html(url)
    data_ids = re.findall(r'data-index="\d+"\s*data-id=(\d+)', html)
    for data_id in data_ids:
        yinyuetai_download('http://v.yinyuetai.com/video/' + data_id,
                           output_dir=output_dir, merge=merge, info_only=info_only)

site_info = "YinYueTai.com"
download = yinyuetai_download
download_playlist = yinyuetai_download_playlist
