#!/usr/bin/env python

__all__ = ['funshion_download']

from ..common import *
import urllib.error
import json

#----------------------------------------------------------------------
def funshion_download(url, output_dir = '.', merge = False, info_only = False, **kwargs):
    """"""
    if re.match(r'http://www.fun.tv/vplay/v-(\w+)', url):  #single video
        funshion_download_by_url(url, output_dir = '.', merge = False, info_only = False)
    elif re.match(r'http://www.fun.tv/vplay/g-(\w+)', url):  #whole drama
        funshion_download_by_drama_url(url, output_dir = '.', merge = False, info_only = False)
    else:
        return

# Logics for single video until drama
#----------------------------------------------------------------------
def funshion_download_by_url(url, output_dir = '.', merge = False, info_only = False):
    """lots of stuff->None
    Main wrapper for single video download.
    """
    if re.match(r'http://www.fun.tv/vplay/v-(\w+)', url):
        match = re.search(r'http://www.fun.tv/vplay/v-(\d+)(.?)', url)
    vid = match.group(1)
    funshion_download_by_vid(vid, output_dir = '.', merge = False, info_only = False)

#----------------------------------------------------------------------
def funshion_download_by_vid(vid, output_dir = '.', merge = False, info_only = False):
    """vid->None
    Secondary wrapper for single video download.
    """
    title = funshion_get_title_by_vid(vid)
    url_list = funshion_vid_to_urls(vid)
    
    for url in url_list:
        type, ext, size = url_info(url)
        print_info(site_info, title, type, size)
    
    if not info_only:
        download_urls(url_list, title, ext, total_size=None, output_dir=output_dir, merge=merge)

#----------------------------------------------------------------------
def funshion_get_title_by_vid(vid):
    """vid->str
    Single video vid to title."""
    html = get_content('http://pv.funshion.com/v5/video/profile?id={vid}&cl=aphone&uc=5'.format(vid = vid))
    c = json.loads(html)
    return c['name']

#----------------------------------------------------------------------
def funshion_vid_to_urls(vid):
    """str->str
    Select one resolution for single video download."""
    html = get_content('http://pv.funshion.com/v5/video/play/?id={vid}&cl=aphone&uc=5'.format(vid = vid))
    return select_url_from_video_api(html)

#Logics for drama until helper functions
#----------------------------------------------------------------------
def funshion_download_by_drama_url(url, output_dir = '.', merge = False, info_only = False):
    """str->None
    url = 'http://www.fun.tv/vplay/g-95785/'
    """
    if re.match(r'http://www.fun.tv/vplay/g-(\w+)', url):
        match = re.search(r'http://www.fun.tv/vplay/g-(\d+)(.?)', url)
    id = match.group(1)
    
    video_list = funshion_drama_id_to_vid(id)
    
    for video in video_list:
        funshion_download_by_id((video[0], id), output_dir = '.', merge = False, info_only = False)
        # id is for drama, vid not the same as the ones used in single video

#----------------------------------------------------------------------
def funshion_download_by_id(vid_id_tuple, output_dir = '.', merge = False, info_only = False):
    """single_episode_id, drama_id->None
    Secondary wrapper for single drama video download.
    """
    (vid, id) = vid_id_tuple
    title = funshion_get_title_by_id(vid, id)
    url_list = funshion_id_to_urls(vid)
    
    for url in url_list:
        type, ext, size = url_info(url)
        print_info(site_info, title, type, size)
    
    if not info_only:
        download_urls(url_list, title, ext, total_size=None, output_dir=output_dir, merge=merge)

#----------------------------------------------------------------------
def funshion_drama_id_to_vid(episode_id):
    """int->[(int,int),...]
    id: 95785
    ->[('626464', '1'), ('626466', '2'), ('626468', '3'),...
    Drama ID to vids used in drama.
    
    **THIS VID IS NOT THE SAME WITH THE ONES USED IN SINGLE VIDEO!!**
    """
    html = get_content('http://pm.funshion.com/v5/media/episode?id={episode_id}&cl=aphone&uc=5'.format(episode_id = episode_id))
    c = json.loads(html)
    #{'definition': [{'name': '流畅', 'code': 'tv'}, {'name': '标清', 'code': 'dvd'}, {'name': '高清', 'code': 'hd'}], 'retmsg': 'ok', 'total': '32', 'sort': '1', 'prevues': [], 'retcode': '200', 'cid': '2', 'template': 'grid', 'episodes': [{'num': '1', 'id': '624728', 'still': None, 'name': '第1集', 'duration': '45:55'}, ], 'name': '太行山上', 'share': 'http://pm.funshion.com/v5/media/share?id=201554&num=', 'media': '201554'}
    return [(i['id'], i['num']) for i in c['episodes']]

#----------------------------------------------------------------------
def funshion_id_to_urls(id):
    """int->list of URL
    Select video URL for single drama video.
    """
    html = get_content('http://pm.funshion.com/v5/media/play/?id={id}&cl=aphone&uc=5'.format(id = id))
    return select_url_from_video_api(html)

#----------------------------------------------------------------------
def funshion_get_title_by_id(single_episode_id, drama_id):
    """single_episode_id, drama_id->str
    This is for full drama.
    Get title for single drama video."""
    html = get_content('http://pm.funshion.com/v5/media/episode?id={id}&cl=aphone&uc=5'.format(id = drama_id))
    c = json.loads(html)
    
    for i in c['episodes']:
        if i['id'] == str(single_episode_id):
            return c['name'] + ' - ' + i['name']

# Helper functions.
#----------------------------------------------------------------------
def select_url_from_video_api(html):
    """str(html)->str(url)
    
    Choose the best one.
    
    Used in both single and drama download.
    
    code definition:
    {'tv': 'liuchang',
    'dvd': 'biaoqing',
    'hd': 'gaoqing',
    'sdvd': 'chaoqing'}"""
    c = json.loads(html)
    #{'retmsg': 'ok', 'retcode': '200', 'selected': 'tv', 'mp4': [{'filename': '', 'http': 'http://jobsfe.funshion.com/query/v1/mp4/7FCD71C58EBD4336DF99787A63045A8F3016EC51.json', 'filesize': '96748671', 'code': 'tv', 'name': '流畅', 'infohash': '7FCD71C58EBD4336DF99787A63045A8F3016EC51'}...], 'episode': '626464'}
    video_dic = {}
    for i in c['mp4']:
        video_dic[i['code']] = i['http']
    quality_preference_list = ['sdvd', 'hd', 'dvd', 'sd']
    url = [video_dic[quality] for quality in quality_preference_list if quality in video_dic][0]
    html = get_html(url)
    c = json.loads(html)
    #'{"return":"succ","client":{"ip":"107.191.**.**","sp":"0","loc":"0"},"playlist":[{"bits":"1638400","tname":"dvd","size":"555811243","urls":["http:\\/\\/61.155.217.4:80\\/play\\/1E070CE31DAA1373B667FD23AA5397C192CA6F7F.mp4",...]}]}'
    return [i['urls'][0] for i in c['playlist']]

site_info = "funshion"
download = funshion_download
download_playlist = playlist_not_supported('funshion')
