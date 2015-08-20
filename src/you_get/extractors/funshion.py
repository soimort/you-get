#!/usr/bin/env python

__all__ = ['funshion_download']

from ..common import *
import urllib.error
import json

#----------------------------------------------------------------------
def funshion_download_by_drama_url(url):
    """str->None
    url = 'http://www.fun.tv/vplay/g-95785/'
    """
    if re.match(r'http://www.fun.tv/vplay/g-(\w+)', url):
        match = re.search(r'http://www.fun.tv/vplay/g-(\d+)(.?)', url)
    id = match.group(1)
    video_list = funshion_drama_id_to_vid(id)
    for video in video_list:
        funshion_download_by_vid(vid)

#----------------------------------------------------------------------
def funshion_drama_id_to_vid(id):
    """int->[(int,int),...]
    id: 95785
    ->[('626464', '1'), ('626466', '2'), ('626468', '3'),...
    """
    html = get_content('http://pm.funshion.com/v5/media/episode?id={episode_id}&cl=aphone&uc=5'.format(episode_id = episode_id))
    c = json.loads(html)
    #{'definition': [{'name': '流畅', 'code': 'tv'}, {'name': '标清', 'code': 'dvd'}, {'name': '高清', 'code': 'hd'}], 'retmsg': 'ok', 'total': '32', 'sort': '1', 'prevues': [], 'retcode': '200', 'cid': '2', 'template': 'grid', 'episodes': [{'num': '1', 'id': '624728', 'still': None, 'name': '第1集', 'duration': '45:55'}, ], 'name': '太行山上', 'share': 'http://pm.funshion.com/v5/media/share?id=201554&num=', 'media': '201554'}
    return [(i['id'], i['num']) for i in c['episodes']]

#----------------------------------------------------------------------
def funshion_vid_to_urls(vid):
    """int->list of URL
    Choose the best one.
    
    code definition:
    {'tv': 'liuchang',
    'dvd': 'biaoqing',
    'hd': 'gaoqing',
    'sdvd': 'chaoqing'}
    """
    html = get_content('http://pm.funshion.com/v5/media/play/?id={vid}&cl=aphone&uc=5'.format(vid = vid))
    c = json.loads(html)
    #{'retmsg': 'ok', 'retcode': '200', 'selected': 'tv', 'mp4': [{'filename': '', 'http': 'http://jobsfe.funshion.com/query/v1/mp4/7FCD71C58EBD4336DF99787A63045A8F3016EC51.json', 'filesize': '96748671', 'code': 'tv', 'name': '流畅', 'infohash': '7FCD71C58EBD4336DF99787A63045A8F3016EC51'}...], 'episode': '626464'}
    video_dic = {}
    url = ''
    for i in c['mp4']:
        video_dic[i['code']] = i['http']
    if 'sdvd' in video_dic:
        url = video_dic['hd']
    elif 'hd' in video_dic:
        url = video_dic['hd']
    elif 'dvd' in video_dic:
        url = video_dic['dvd']
    elif 'sd' in video_dic:
        url = video_dic['sd']
    html = get_html(url)
    c = json.loads(html)
    #'{"return":"succ","client":{"ip":"107.191.**.**","sp":"0","loc":"0"},"playlist":[{"bits":"1638400","tname":"dvd","size":"555811243","urls":["http:\\/\\/61.155.217.4:80\\/play\\/1E070CE31DAA1373B667FD23AA5397C192CA6F7F.mp4",...]}]}'
    return [i['urls'][0] for i in c['playlist']]

#----------------------------------------------------------------------
def funshion_get_title_by_vid(vid):
    """int->str"""
    #http://pm.funshion.com/v5/media/profile?id=109229&cl=aphone&uc=5
    html = get_content('http://pm.funshion.com/v5/media/profile?id={vid}&cl=aphone&uc=5'.format(vid = vid))
    c = json.loads(html)
    return c['name']

#----------------------------------------------------------------------
def funshion_download_by_url(url, output_dir = '.', merge = False, info_only = False):
    if re.match(r'http://www.fun.tv/vplay/v-(\w+)', url):
        match = re.search(r'http://www.fun.tv/vplay/v-(\d+)(.?)', url)
    vid = match.group(1)
    title = funshion_get_title_by_vid(vid)
    url_list = funshion_vid_to_urls(vid)
    for url in url_list:
        type, ext, size = url_info(url)
        print_info(site_info, title, type_, size)
        if not info_only:
            download_urls(url_list, title, type_, total_size=None, output_dir=output_dir, merge=merge)

site_info = "fun.tv/Funshion"
download = funshion_download
download_playlist = playlist_not_supported('funshion')