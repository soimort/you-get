#!/usr/bin/env python

__all__ = ['bilibili_download']

import hashlib
import re
import time
import json
import http.cookiejar
import urllib.request
import urllib.parse
from xml.dom.minidom import parseString

from ..common import *
from ..util.log import *
from ..extractor import *

from .qq import qq_download_by_vid
from .sina import sina_download_by_vid
from .tudou import tudou_download_by_id
from .youku import youku_download_by_vid

class Bilibili(VideoExtractor):
    name = 'Bilibili'
    live_api = 'http://live.bilibili.com/api/playurl?cid={}&otype=json'
    api_url = 'http://interface.bilibili.com/v2/playurl?'
    bangumi_api_url = 'http://bangumi.bilibili.com/player/web_api/playurl?'
    live_room_init_api_url = 'https://api.live.bilibili.com/room/v1/Room/room_init?id={}'
    live_room_info_api_url = 'https://api.live.bilibili.com/room/v1/Room/get_info?room_id={}'

    #SEC1 = '1c15888dc316e05a15fdd0a02ed6584f'
    SEC1 = '94aba54af9065f71de72f5508f1cd42e'
    SEC2 = '9b288147e5474dd2aa67085f716c560d'
    stream_types = [
        {'id': 'hdflv'},
        {'id': 'flv720'},
        {'id': 'flv'},
        {'id': 'hdmp4'},
        {'id': 'mp4'},
        {'id': 'live'},
        {'id': 'vc'}
    ]
    fmt2qlt = dict(hdflv=4, flv=3, hdmp4=2, mp4=1)

    @staticmethod
    def bilibili_stream_type(urls):
        url = urls[0]
        if 'hd.flv' in url or '-80.flv' in url:
            return 'hdflv', 'flv'
        if '-64.flv' in url:
            return 'flv720', 'flv'
        if '.flv' in url:
            return 'flv', 'flv'
        if 'hd.mp4' in url or '-48.mp4' in url:
            return 'hdmp4', 'mp4'
        if '.mp4' in url:
            return 'mp4', 'mp4'
        raise Exception('Unknown stream type')

    def api_req(self, cid, quality, bangumi, bangumi_movie=False, **kwargs):
        ts = str(int(time.time()))
        if not bangumi:
            #params_str = 'cid={}&player=1&quality={}&ts={}'.format(cid, quality, ts)
            params_str = 'appkey=84956560bc028eb7&cid={}&otype=xml&qn={}&quality={}&type='.format(cid, quality, quality)
            chksum = hashlib.md5(bytes(params_str+self.SEC1, 'utf8')).hexdigest()
            api_url = self.api_url + params_str + '&sign=' + chksum
        else:
            mod = 'movie' if bangumi_movie else 'bangumi'
            params_str = 'cid={}&module={}&player=1&quality={}&ts={}'.format(cid, mod, quality, ts)
            chksum = hashlib.md5(bytes(params_str+self.SEC2, 'utf8')).hexdigest()
            api_url = self.bangumi_api_url + params_str + '&sign=' + chksum

        xml_str = get_content(api_url, headers={'referer': self.url, 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'})
        return xml_str

    def parse_bili_xml(self, xml_str):
        urls_list = []
        total_size = 0
        doc = parseString(xml_str.encode('utf8'))
        durls = doc.getElementsByTagName('durl')
        for durl in durls:
            size = durl.getElementsByTagName('size')[0]
            total_size += int(size.firstChild.nodeValue)
            url = durl.getElementsByTagName('url')[0]
            urls_list.append(url.firstChild.nodeValue)
        stream_type, container = self.bilibili_stream_type(urls_list)
        if stream_type not in self.streams:
            self.streams[stream_type] = {}
            self.streams[stream_type]['src'] = urls_list
            self.streams[stream_type]['size'] = total_size
            self.streams[stream_type]['container'] = container

    def download_by_vid(self, cid, bangumi, **kwargs):
        stream_id = kwargs.get('stream_id')
        # guard here. if stream_id invalid, fallback as not stream_id
        if stream_id and stream_id in self.fmt2qlt:
            quality = stream_id
        else:
            quality = 'hdflv' if bangumi else 'flv'

        info_only = kwargs.get('info_only')
        for qlt in [116,112,80,74,64,32,16,15]:
            api_xml = self.api_req(cid, qlt, bangumi, **kwargs)
            self.parse_bili_xml(api_xml)
        if not info_only or stream_id:
            self.danmuku = get_danmuku_xml(cid)

    def prepare(self, **kwargs):
        if socket.getdefaulttimeout() == 600: # no timeout specified
            socket.setdefaulttimeout(2) # fail fast, very speedy!

        # handle "watchlater" URLs
        if '/watchlater/' in self.url:
            aid = re.search(r'av(\d+)', self.url).group(1)
            self.url = 'http://www.bilibili.com/video/av{}/'.format(aid)

        self.ua = fake_headers['User-Agent']
        self.url = url_locations([self.url], faker=True)[0]
        frag = urllib.parse.urlparse(self.url).fragment
        # http://www.bilibili.com/video/av3141144/index_2.html#page=3
        if frag:
            hit = re.search(r'page=(\d+)', frag)
            if hit is not None:
                page = hit.group(1)
                aid = re.search(r'av(\d+)', self.url).group(1)
                self.url = 'http://www.bilibili.com/video/av{}/index_{}.html'.format(aid, page)
        self.referer = self.url
        self.page = get_content(self.url, headers=fake_headers)

        m = re.search(r'<h1.*?>(.*?)</h1>', self.page) or re.search(r'<h1 title="([^"]+)">', self.page)
        if m is not None:
            self.title = m.group(1)
            s = re.search(r'<span>([^<]+)</span>', m.group(1))
            if s:
                self.title = unescape_html(s.group(1))
        if self.title is None:
            m = re.search(r'property="og:title" content="([^"]+)"', self.page)
            if m is not None:
                self.title = m.group(1)

        if 'subtitle' in kwargs:
            subtitle = kwargs['subtitle']
            self.title = '{} {}'.format(self.title, subtitle)
        else:
            playinfo = re.search(r'__INITIAL_STATE__=(.*?);\(function\(\)', self.page)
            if playinfo is not None:
                jsonPlayinfo = json.loads(playinfo.group(1))
                if 'videoData' in jsonPlayinfo:
                    pages = jsonPlayinfo['videoData']['pages']
                    if len(pages) > 1:
                        qs = dict(parse.parse_qsl(urllib.parse.urlparse(self.url).query))
                        page = pages[int(qs.get('p', 1)) - 1]
                        self.title = '{} #{}. {}'.format(self.title, page['page'], page['part'])

        if 'bangumi.bilibili.com/movie' in self.url:
            self.movie_entry(**kwargs)
        elif 'bangumi.bilibili.com' in self.url:
            self.bangumi_entry(**kwargs)
        elif 'bangumi/' in self.url:
            self.bangumi_entry(**kwargs)
        elif 'live.bilibili.com' in self.url:
            self.live_entry(**kwargs)
        elif 'vc.bilibili.com' in self.url:
            self.vc_entry(**kwargs)
        else:
            self.entry(**kwargs)

    def movie_entry(self, **kwargs):
        patt = r"var\s*aid\s*=\s*'(\d+)'"
        aid = re.search(patt, self.page).group(1)
        page_list = json.loads(get_content('http://www.bilibili.com/widget/getPageList?aid={}'.format(aid)))
        # better ideas for bangumi_movie titles?
        self.title = page_list[0]['pagename']
        self.download_by_vid(page_list[0]['cid'], True, bangumi_movie=True, **kwargs)

    def entry(self, **kwargs):
        # tencent player
        tc_flashvars = re.search(r'"bili-cid=\d+&bili-aid=\d+&vid=([^"]+)"', self.page)
        if tc_flashvars:
            tc_flashvars = tc_flashvars.group(1)
        if tc_flashvars is not None:
            self.out = True
            qq_download_by_vid(tc_flashvars, self.title, True, output_dir=kwargs['output_dir'], merge=kwargs['merge'], info_only=kwargs['info_only'])
            return

        has_plist = re.search(r'"page":2', self.page)
        if has_plist and not kwargs.get('playlist'):
            log.w('This page contains a playlist. (use --playlist to download all videos.)')

        try:
            page_list = json.loads(re.search(r'"pages":(\[.*?\])', self.page).group(1))
            index_id = int(re.search(r'index_(\d+)', self.url).group(1))
            cid = page_list[index_id-1]['cid'] # change cid match rule
        except:
            cid = re.search(r'"cid":(\d+)', self.page).group(1)
        if cid is not None:
            self.download_by_vid(cid, re.search('bangumi', self.url) is not None, **kwargs)
        else:
            # flashvars?
            flashvars = re.search(r'flashvars="([^"]+)"', self.page).group(1)
            if flashvars is None:
                raise Exception('Unsupported page {}'.format(self.url))
            param = flashvars.split('&')[0]
            t, cid = param.split('=')
            t = t.strip()
            cid = cid.strip()
            if t == 'vid':
                sina_download_by_vid(cid, self.title, output_dir=kwargs['output_dir'], merge=kwargs['merge'], info_only=kwargs['info_only'])
            elif t == 'ykid':
                youku_download_by_vid(cid, self.title, output_dir=kwargs['output_dir'], merge=kwargs['merge'], info_only=kwargs['info_only'])
            elif t == 'uid':
                tudou_download_by_id(cid, self.title, output_dir=kwargs['output_dir'], merge=kwargs['merge'], info_only=kwargs['info_only'])
            else:
                raise NotImplementedError('Unknown flashvars {}'.format(flashvars))
            return

    def live_entry(self, **kwargs):
        # Extract room ID from the short display ID (seen in the room
        # URL). The room ID is usually the same as the short ID, but not
        # always; case in point: https://live.bilibili.com/48, with 48
        # as the short ID and 63727 as the actual ID.
        room_short_id = re.search(r'live.bilibili.com/([^?]+)', self.url).group(1)
        room_init_api_response = json.loads(get_content(self.live_room_init_api_url.format(room_short_id)))
        self.room_id = room_init_api_response['data']['room_id']

        room_info_api_response = json.loads(get_content(self.live_room_info_api_url.format(self.room_id)))
        self.title = room_info_api_response['data']['title']

        api_url = self.live_api.format(self.room_id)
        json_data = json.loads(get_content(api_url))
        urls = [json_data['durl'][0]['url']]

        self.streams['live'] = {}
        self.streams['live']['src'] = urls
        self.streams['live']['container'] = 'flv'
        self.streams['live']['size'] = 0

    def vc_entry(self, **kwargs):
        vc_id = re.search(r'video/(\d+)', self.url)
        if not vc_id:
            vc_id = re.search(r'vcdetail\?vc=(\d+)', self.url)
            if not vc_id:
                log.wtf('Unknown url pattern')
        endpoint = 'http://api.vc.bilibili.com/clip/v1/video/detail?video_id={}&need_playurl=1'.format(vc_id.group(1))
        vc_meta = json.loads(get_content(endpoint, headers=fake_headers))
        if vc_meta['code'] != 0:
            log.wtf('{}\n{}'.format(vc_meta['msg'], vc_meta['message']))
        item = vc_meta['data']['item']
        self.title = item['description']

        self.streams['vc'] = {}
        self.streams['vc']['src'] = [item['video_playurl']]
        self.streams['vc']['container'] = 'mp4'
        self.streams['vc']['size'] = int(item['video_size'])

    def bangumi_entry(self, **kwargs):
        bangumi_id = re.search(r'(\d+)', self.url).group(1)
        frag = urllib.parse.urlparse(self.url).fragment
        if frag:
            episode_id = frag
        else:
            episode_id = re.search(r'first_ep_id\s*=\s*"(\d+)"', self.page) or re.search(r'\/ep(\d+)', self.url).group(1)
        # cont = post_content('http://bangumi.bilibili.com/web_api/get_source', post_data=dict(episode_id=episode_id))
        # cid = json.loads(cont)['result']['cid']
        cont = get_content('http://bangumi.bilibili.com/web_api/episode/{}.json'.format(episode_id))
        ep_info = json.loads(cont)['result']['currentEpisode']

        bangumi_data = get_bangumi_info(str(ep_info['seasonId']))
        bangumi_payment = bangumi_data.get('payment')
        if bangumi_payment and bangumi_payment['price'] != '0':
            log.w("It's a paid item")
        # ep_ids = collect_bangumi_epids(bangumi_data)

        index_title = ep_info['indexTitle']
        long_title = ep_info['longTitle'].strip()
        cid = ep_info['danmaku']

        self.title = '{} [{} {}]'.format(self.title, index_title, long_title)
        self.download_by_vid(cid, bangumi=True, **kwargs)


def check_oversea():
    url = 'https://interface.bilibili.com/player?id=cid:17778881'
    xml_lines = get_content(url).split('\n')
    for line in xml_lines:
        key = line.split('>')[0][1:]
        if key == 'country':
            value = line.split('>')[1].split('<')[0]
            if value != '中国':
                return True
            else:
                return False
    return False

def check_sid():
    if not cookies:
        return False
    for cookie in cookies:
        if cookie.domain == '.bilibili.com' and cookie.name == 'sid':
            return True
    return False

def fetch_sid(cid, aid):
    url = 'http://interface.bilibili.com/player?id=cid:{}&aid={}'.format(cid, aid)
    cookies = http.cookiejar.CookieJar()
    req = urllib.request.Request(url)
    res = urllib.request.urlopen(url)
    cookies.extract_cookies(res, req)
    for c in cookies:
        if c.domain == '.bilibili.com' and c.name == 'sid':
            return c.value
    raise

def collect_bangumi_epids(json_data):
    eps = json_data['episodes'][::-1]
    return [ep['episode_id'] for ep in eps]

def get_bangumi_info(season_id):
    BASE_URL = 'http://bangumi.bilibili.com/jsonp/seasoninfo/'
    long_epoch = int(time.time() * 1000)
    req_url = BASE_URL + season_id + '.ver?callback=seasonListCallback&jsonp=jsonp&_=' + str(long_epoch)
    season_data = get_content(req_url)
    season_data = season_data[len('seasonListCallback('):]
    season_data = season_data[: -1 * len(');')]
    json_data = json.loads(season_data)
    return json_data['result']

def get_danmuku_xml(cid):
    return get_content('http://comment.bilibili.com/{}.xml'.format(cid))

def parse_cid_playurl(xml):
    from xml.dom.minidom import parseString
    try:
        urls_list = []
        total_size = 0
        doc = parseString(xml.encode('utf-8'))
        durls = doc.getElementsByTagName('durl')
        cdn_cnt = len(durls[0].getElementsByTagName('url'))
        for i in range(cdn_cnt):
            urls_list.append([])
        for durl in durls:
            size = durl.getElementsByTagName('size')[0]
            total_size += int(size.firstChild.nodeValue)
            cnt = len(durl.getElementsByTagName('url'))
            for i in range(cnt):
                u = durl.getElementsByTagName('url')[i].firstChild.nodeValue
                urls_list[i].append(u)
        return urls_list, total_size
    except Exception as e:
        log.w(e)
        return [], 0

def download_video_from_favlist(url, **kwargs):
    # the url has format: https://space.bilibili.com/64169458/#/favlist?fid=1840028

    m = re.search(r'space\.bilibili\.com/(\d+)/.*?fid=(\d+).*?', url)
    vmid = ""
    favid = ""
    if m is not None:
        vmid = m.group(1)
        favid = m.group(2)
        jsonresult = json.loads(get_content("https://api.bilibili.com/x/space/fav/arc?vmid={}&ps=300&fid={}&order=fav_time&tid=0&keyword=&pn=1&jsonp=jsonp".format(vmid, favid)))

        # log.wtf("Got files list for vmid" + vmid + " favid:" + favid)
        if jsonresult['code'] != 0:
            log.wtf("Fail to get the files of page " + jsonresult)
            sys.exit(2)

        else:
            videos = jsonresult['data']['archives']
            videocount = len(videos)
            for i in range(videocount):
                videoid = videos[i]["aid"]
                videotitle = videos[i]["title"]
                videourl = "https://www.bilibili.com/video/av{}".format(videoid)
                print("Start downloading ", videotitle, " video ", videotitle)
                Bilibili().download_by_url(videourl, subtitle=videotitle, **kwargs)

    else:
        log.wtf("Fail to parse the fav title" + url, "")


def bilibili_download_playlist_by_url(url, **kwargs):
    url = url_locations([url], faker=True)[0]
    kwargs['playlist'] = True
    # a bangumi here? possible?
    if 'live.bilibili' in url:
        site.download_by_url(url)
    elif 'bangumi.bilibili' in url:
        bangumi_id = re.search(r'(\d+)', url).group(1)
        bangumi_data = get_bangumi_info(bangumi_id)
        ep_ids = collect_bangumi_epids(bangumi_data)

        base_url = url.split('#')[0]
        for ep_id in ep_ids:
            ep_url = '#'.join([base_url, ep_id])
            Bilibili().download_by_url(ep_url, **kwargs)
    elif 'favlist' in url:
        # this a fav list folder
        download_video_from_favlist(url, **kwargs)
    else:
        aid = re.search(r'av(\d+)', url).group(1)
        page_list = json.loads(get_content('http://www.bilibili.com/widget/getPageList?aid={}'.format(aid)))
        page_cnt = len(page_list)
        for no in range(1, page_cnt+1):
            page_url = 'http://www.bilibili.com/video/av{}/index_{}.html'.format(aid, no)
            subtitle = '#%s. %s'% (page_list[no-1]['page'], page_list[no-1]['pagename'])
            Bilibili().download_by_url(page_url, subtitle=subtitle, **kwargs)

site = Bilibili()
download = site.download_by_url
download_playlist = bilibili_download_playlist_by_url

bilibili_download = download
