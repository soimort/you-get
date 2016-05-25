__all__ = ['embed_download']

from ..common import *

from .iqiyi import iqiyi_download_by_vid
from .le import letvcloud_download_by_vu
from .netease import netease_download
from .qq import qq_download_by_vid
from .sina import sina_download_by_vid
from .tudou import tudou_download_by_id
from .vimeo import vimeo_download_by_id
from .yinyuetai import yinyuetai_download_by_id
from .youku import youku_download_by_vid

"""
refer to http://open.youku.com/tools
"""
youku_embed_patterns = [ 'youku\.com/v_show/id_([a-zA-Z0-9=]+)',
                         'player\.youku\.com/player\.php/sid/([a-zA-Z0-9=]+)/v\.swf',
                         'loader\.swf\?VideoIDS=([a-zA-Z0-9=]+)',
                         'player\.youku\.com/embed/([a-zA-Z0-9=]+)',
                         'YKU.Player\(\'[a-zA-Z0-9]+\',{ client_id: \'[a-zA-Z0-9]+\', vid: \'([a-zA-Z0-9]+)\''
                       ]

"""
http://www.tudou.com/programs/view/html5embed.action?type=0&amp;code=3LS_URGvl54&amp;lcode=&amp;resourceId=0_06_05_99
"""
tudou_embed_patterns = [ 'tudou\.com[a-zA-Z0-9\/\?=\&\.\;]+code=([a-zA-Z0-9_]+)\&',
                         'www\.tudou\.com/v/([a-zA-Z0-9_-]+)/[^"]*v\.swf'
                       ]

"""
refer to http://open.tudou.com/wiki/video/info
"""
tudou_api_patterns = [ ]

yinyuetai_embed_patterns = [ 'player\.yinyuetai\.com/video/swf/(\d+)' ]

iqiyi_embed_patterns = [ 'player\.video\.qiyi\.com/([^/]+)/[^/]+/[^/]+/[^/]+\.swf[^"]+tvId=(\d+)' ]

netease_embed_patterns = [ '(http://\w+\.163\.com/movie/[^\'"]+)' ]

vimeo_embed_patters = [ 'player\.vimeo\.com/video/(\d+)' ]


def embed_download(url, output_dir = '.', merge = True, info_only = False ,**kwargs):
    content = get_content(url, headers=fake_headers)
    found = False
    title = match1(content, '<title>([^<>]+)</title>')

    vids = matchall(content, youku_embed_patterns)
    for vid in set(vids):
        found = True
        youku_download_by_vid(vid, title=title, output_dir=output_dir, merge=merge, info_only=info_only)

    vids = matchall(content, tudou_embed_patterns)
    for vid in set(vids):
        found = True
        tudou_download_by_id(vid, title=title, output_dir=output_dir, merge=merge, info_only=info_only)

    vids = matchall(content, yinyuetai_embed_patterns)
    for vid in vids:
        found = True
        yinyuetai_download_by_id(vid, title=title, output_dir=output_dir, merge=merge, info_only=info_only)

    vids = matchall(content, iqiyi_embed_patterns)
    for vid in vids:
        found = True
        iqiyi_download_by_vid((vid[1], vid[0]), title=title, output_dir=output_dir, merge=merge, info_only=info_only)

    urls = matchall(content, netease_embed_patterns)
    for url in urls:
        found = True
        netease_download(url, title=title, output_dir=output_dir, merge=merge, info_only=info_only)

    urls = matchall(content, vimeo_embed_patters)
    for url in urls:
        found = True
        vimeo_download_by_id(url, title=title, output_dir=output_dir, merge=merge, info_only=info_only)

    if not found:
        raise NotImplementedError(url)

site_info = "any.any"
download = embed_download
download_playlist = playlist_not_supported('any.any')
