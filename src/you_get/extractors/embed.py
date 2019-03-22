__all__ = ['embed_download']

import urllib.parse

from ..common import *

from .bilibili import bilibili_download
from .dailymotion import dailymotion_download
from .iqiyi import iqiyi_download_by_vid
from .le import letvcloud_download_by_vu
from .netease import netease_download
from .qq import qq_download_by_vid
from .sina import sina_download_by_vid
from .tudou import tudou_download_by_id
from .vimeo import vimeo_download_by_id
from .yinyuetai import yinyuetai_download_by_id
from .youku import youku_download_by_vid
from . import iqiyi
from . import bokecc

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
tudou_embed_patterns = [ 'tudou\.com[a-zA-Z0-9\/\?=\&\.\;]+code=([a-zA-Z0-9_-]+)\&',
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

dailymotion_embed_patterns = [ 'www\.dailymotion\.com/embed/video/(\w+)' ]

"""
check the share button on http://www.bilibili.com/video/av5079467/
"""
bilibili_embed_patterns = [ 'static\.hdslb\.com/miniloader\.swf.*aid=(\d+)' ]


'''
http://open.iqiyi.com/lib/player.html
'''
iqiyi_patterns = [r'(?:\"|\')(https?://dispatcher\.video\.qiyi\.com\/disp\/shareplayer\.swf\?.+?)(?:\"|\')',
                  r'(?:\"|\')(https?://open\.iqiyi\.com\/developer\/player_js\/coopPlayerIndex\.html\?.+?)(?:\"|\')']

bokecc_patterns = [r'bokecc\.com/flash/pocle/player\.swf\?siteid=(.+?)&vid=(.{32})']

recur_limit = 3


def embed_download(url, output_dir = '.', merge = True, info_only = False, **kwargs):
    content = get_content(url, headers=fake_headers)
    found = False
    title = match1(content, '<title>([^<>]+)</title>')

    vids = matchall(content, youku_embed_patterns)
    for vid in set(vids):
        found = True
        youku_download_by_vid(vid, title=title, output_dir=output_dir, merge=merge, info_only=info_only, **kwargs)

    vids = matchall(content, tudou_embed_patterns)
    for vid in set(vids):
        found = True
        tudou_download_by_id(vid, title=title, output_dir=output_dir, merge=merge, info_only=info_only, **kwargs)

    vids = matchall(content, yinyuetai_embed_patterns)
    for vid in vids:
        found = True
        yinyuetai_download_by_id(vid, title=title, output_dir=output_dir, merge=merge, info_only=info_only, **kwargs)

    vids = matchall(content, iqiyi_embed_patterns)
    for vid in vids:
        found = True
        iqiyi_download_by_vid((vid[1], vid[0]), title=title, output_dir=output_dir, merge=merge, info_only=info_only, **kwargs)

    urls = matchall(content, netease_embed_patterns)
    for url in urls:
        found = True
        netease_download(url, output_dir=output_dir, merge=merge, info_only=info_only, **kwargs)

    urls = matchall(content, vimeo_embed_patters)
    for url in urls:
        found = True
        vimeo_download_by_id(url, title=title, output_dir=output_dir, merge=merge, info_only=info_only, referer=url, **kwargs)

    urls = matchall(content, dailymotion_embed_patterns)
    for url in urls:
        found = True
        dailymotion_download(url, output_dir=output_dir, merge=merge, info_only=info_only, **kwargs)

    aids = matchall(content, bilibili_embed_patterns)
    for aid in aids:
        found = True
        url = 'http://www.bilibili.com/video/av%s/' % aid
        bilibili_download(url, output_dir=output_dir, merge=merge, info_only=info_only, **kwargs)

    iqiyi_urls = matchall(content, iqiyi_patterns)
    for url in iqiyi_urls:
        found = True
        iqiyi.download(url, output_dir=output_dir, merge=merge, info_only=info_only, **kwargs)

    bokecc_metas = matchall(content, bokecc_patterns)
    for meta in bokecc_metas:
        found = True
        bokecc.bokecc_download_by_id(meta[1], output_dir=output_dir, merge=merge, info_only=info_only, **kwargs)

    if found:
        return True

    # Try harder, check all iframes
    if 'recur_lv' not in kwargs or kwargs['recur_lv'] < recur_limit:
        r = kwargs.get('recur_lv')
        if r is None:
            r = 1
        else:
            r += 1
        iframes = matchall(content, [r'<iframe.+?src=(?:\"|\')(.+?)(?:\"|\')'])
        for iframe in iframes:
            if not iframe.startswith('http'):
                src = urllib.parse.urljoin(url, iframe)
            else:
                src = iframe
            found = embed_download(src, output_dir=output_dir, merge=merge, info_only=info_only, recur_lv=r, **kwargs)
            if found:
                return True

    if not found and 'recur_lv' not in kwargs:
        raise NotImplementedError(url)
    else:
        return found

site_info = "any.any"
download = embed_download
download_playlist = playlist_not_supported('any.any')
