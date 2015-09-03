__all__ = ['embed_download']

from ..common import *

from .letv import letvcloud_download_by_vu
from .qq import qq_download_by_vid
from .sina import sina_download_by_vid
from .tudou import tudou_download_by_id
from .youku import youku_download_by_vid
from .youku import Youku

"""
refer to http://open.youku.com/tools
"""
youku_api_pattern = 'YKU.Player\(\'[a-zA-Z0-9]+\',{ client_id: \'[a-zA-Z0-9]+\', vid: \'([a-zA-Z0-9]+)\''
"""
http://www.tudou.com/programs/view/html5embed.action?type=0&amp;code=3LS_URGvl54&amp;lcode=&amp;resourceId=0_06_05_99
"""
tudou_embed_pattern = 'tudou\.com[a-zA-Z0-9\/\?=\&\.\;]+code=([[a-zA-Z0-9_]+)\&'

"""
refer to http://open.tudou.com/wiki/video/info
"""

def embed_download(url, output_dir = '.', merge = True, info_only = False ,**kwargs):
    content = get_content(url)
    found = False
    title = match1(content, '<title>([^<>]+)</title>')
    vid = Youku.get_vid_from_url(content) or \
          match1(content, youku_api_pattern)
    if vid is not None:
        found = True
        youku_download_by_vid(vid, title=title, output_dir=output_dir, merge=merge, info_only=info_only)

    vid = match1(content, tudou_embed_pattern)
    if vid is not None:
        found = True
        tudou_download_by_id(vid, title=title, output_dir=output_dir, merge=merge, info_only=info_only)
    if not found:
        raise NotImplementedError(url)

site_info = "any.any"
download = embed_download
download_playlist = playlist_not_supported('any.any')
