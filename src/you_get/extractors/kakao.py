#!/usr/bin/env python

from ..common import *
from .universal import *

__all__ = ['kakao_download']


def kakao_download(url, output_dir='.', info_only=False,  **kwargs):
    json_request_url = 'https://videofarm.daum.net/controller/api/closed/v1_2/IntegratedMovieData.json?vid={}'

    # in this implementation playlist not supported so use url_without_playlist
    # if want to support playlist need to change that
    if re.search('playlistId', url):
        url = re.search(r"(.+)\?.+?", url).group(1)

    page = get_content(url)
    try:
        vid = re.search(r"<meta name=\"vid\" content=\"(.+)\">", page).group(1)
        title = re.search(r"<meta name=\"title\" content=\"(.+)\">", page).group(1)

        meta_str = get_content(json_request_url.format(vid))
        meta_json = json.loads(meta_str)

        standard_preset = meta_json['output_list']['standard_preset']
        output_videos = meta_json['output_list']['output_list']
        size = ''
        if meta_json['svcname'] == 'smr_pip':
            for v in output_videos:
                if v['preset'] == 'mp4_PIP_SMR_480P':
                    size = int(v['filesize'])
                    break
        else:
            for v in output_videos:
                if v['preset'] == standard_preset:
                    size = int(v['filesize'])
                    break

        video_url = meta_json['location']['url']

        print_info(site_info, title, 'mp4', size)
        if not info_only:
            download_urls([video_url], title, 'mp4', size, output_dir, **kwargs)
    except:
        universal_download(url, output_dir, merge=kwargs['merge'], info_only=info_only, **kwargs)


site_info = "tv.kakao.com"
download = kakao_download
download_playlist = playlist_not_supported('kakao')
