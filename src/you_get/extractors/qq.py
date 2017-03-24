#!/usr/bin/env python
__all__ = ['qq_download']

from ..common import *
from .qie import download as qieDownload, VideoExtractor
from urllib.parse import urlparse, parse_qs
import struct
import base64
import random
import time

DELTA = 0x9e3779b9
ROUNDS = 16

SALT_LEN = 2
ZERO_LEN = 7

SEED = 0xdead


def rand():
    global SEED
    if SEED == 0:
        SEED = 123459876
    k1 = 0xffffffff & (-2836 * (SEED // 127773))
    k2 = 0xffffffff & (16807 * (SEED % 127773))
    SEED = 0xffffffff & (k1 + k2)
    if SEED < 0:
        SEED = SEED + 2147483647
    return SEED


def pack(data):
    target = []
    for i in data:
        target.extend(struct.pack('>I', i))
    return target


def unpack(data):
    data = bytes(data)
    target = []
    for i in range(0, len(data), 4):
        target.extend(struct.unpack('>I', data[i:i + 4]))
    return target


def tea_encrypt(v, key):
    s = 0
    key = unpack(key)
    v = unpack(v)
    for i in range(ROUNDS):
        s += DELTA
        s &= 0xffffffff
        v[0] += (v[1] + s) ^ ((v[1] >> 5) + key[1]) ^ ((v[1] << 4) + key[0])
        v[0] &= 0xffffffff
        v[1] += (v[0] + s) ^ ((v[0] >> 5) + key[3]) ^ ((v[0] << 4) + key[2])
        v[1] &= 0xffffffff
    return pack(v)


def oi_symmetry_encrypt2(raw_data, key):
    pad_salt_body_zero_len = 1 + SALT_LEN + len(raw_data) + ZERO_LEN
    pad_len = pad_salt_body_zero_len % 8
    if pad_len:
        pad_len = 8 - pad_len
    data = []
    data.append(rand() & 0xf8 | pad_len)
    while pad_len + SALT_LEN:
        data.append(rand() & 0xff)
        pad_len = pad_len - 1
    data.extend(raw_data)
    data.extend([0x00] * ZERO_LEN)

    temp = [0x00] * 8
    enc = tea_encrypt(data[:8], key)
    for i in range(8, len(data), 8):
        d1 = data[i:]
        for j in range(8):
            d1[j] = d1[j] ^ enc[i - 8 + j]
        d1 = tea_encrypt(d1, key)
        for j in range(8):
            d1[j] = d1[j] ^ data[i - 8 + j] ^ temp[j]
            enc.append(d1[j])
            temp[j] = enc[i - 8 + j]
    return enc


KEY = [
    0xfa, 0x82, 0xde, 0xb5, 0x2d, 0x4b, 0xba, 0x31,
    0x39, 0x6, 0x33, 0xee, 0xfb, 0xbf, 0xf3, 0xb6
]


def packstr(data):
    l = len(data)
    t = []
    t.append((l & 0xFF00) >> 8)
    t.append(l & 0xFF)
    t.extend([ord(c) for c in data])
    return t


def strsum(data):
    s = 0
    for c in data:
        s = s * 131 + c
    return 0x7fffffff & s


def echo_ckeyv3(vid, guid='', t=None, player_version='3.2.38.401', platform=10902, stdfrom='bcng'):
    data = []
    data.extend(pack([21507, 3168485562]))
    data.extend(pack([platform]))

    if not t:
        t = time.time()
    seconds = int(t)
    microseconds = int(1000000 * (t - int(t)))
    data.extend(pack([microseconds, seconds]))
    data.extend(packstr(stdfrom))

    r = random.random()
    data.extend(packstr('%.16f' % r))
    data.extend(packstr(player_version))
    data.extend(packstr(vid))
    data.extend(packstr('2%s' % guid))
    data.extend(packstr('4null'))
    data.extend(packstr('4null'))
    data.extend([0x00, 0x00, 0x00, 0x01])
    data.extend([0x00, 0x00, 0x00, 0x00])

    l = len(data)
    data.insert(0, l & 0xFF)
    data.insert(0, (l & 0xFF00) >> 8)

    enc = oi_symmetry_encrypt2(data, KEY)

    pad = [0x00, 0x00, 0x00, 0x00, 0xff & rand(), 0xff & rand(), 0xff & rand(), 0xff & rand()]
    pad[0] = pad[4] ^ 71 & 0xFF
    pad[1] = pad[5] ^ -121 & 0xFF
    pad[2] = pad[6] ^ -84 & 0xFF
    pad[3] = pad[7] ^ -86 & 0xFF

    pad.extend(enc)
    pad.extend(pack([strsum(data)]))

    result = base64.b64encode(bytes(pad), b'_-').decode('utf-8').replace('=', '')
    return result


class QQ(VideoExtractor):
    name = "腾讯视频(qq)"

    stream_types = [
        {'id': 'fhd'},
        {'id': 'shd'},
        {'id': 'hd'},
        {'id': 'sd'},
    ]

    def prepare(self, **kwargs):
        # vid = kwargs['vid'] if 'vid' in kwargs else None
        # vid = vid if vid is not None else self.vid
        vid = ('vid' in kwargs and kwargs['vid']) or self.vid
        if vid is None:
            return

        info_api = 'http://vv.video.qq.com/getinfo?otype=json&appver=3%2E2%2E19%2E333&platform=11&defnpayver=1&vid=' + vid
        info = get_html(info_api)
        video_json = json.loads(match1(info, r'QZOutputJson=(.*)')[:-1])
        if 'vl' not in video_json or 'vi' not in video_json['vl']:
            # sys.stderr.writelines('Extract failed!!\n'+info+'\n')
            print('Extract failed!!', info, file=sys.stderr)
            return
        vi0 = video_json['vl']['vi'][0]
        lnk = vi0['lnk']
        self.title = vi0['ti']
        url_prefix = vi0['ul']['ui'][0]['url']
        url_prefix = urlparse(url_prefix)._replace(netloc='lmbsy.qq.com').geturl()  # fast
        # url_prefix = urlparse(url_prefix)._replace(netloc='ugcbsy.qq.com').geturl()  # fast
        # url_prefix = urlparse(url_prefix)._replace(netloc='vmind.qqvideo.tc.qq.com').geturl()  # fast
        fi = video_json['fl']['fi']  # streams
        self.streams = {}

        class LazyDict(dict):
            def __init__(self, stream_id=None, **kwargs):
                dict.__init__(self, **kwargs)
                self.stream_id = stream_id

            def _getfilename(self, lnk, stream_id, idx):
                return '{lnk}.p{num}.{idx}.mp4'.format(lnk=lnk, num=stream_id % 10 ** 3 if stream_id < 10 ** 4 else stream_id % 10 ** 4, idx=idx)

            def _getvkey(self, vid, format, idx):
                import uuid
                appver = '3.2.38.401'
                guid = uuid.uuid4().hex.upper()
                platform = 11
                cKey = echo_ckeyv3(vid=vid, guid=guid, player_version=appver, platform=platform)
                key_api = 'http://vv.video.qq.com/getvkey?vid={vid}&appver={appver}&platform={platform}&otype=json&filename={filename}&format={format}&cKey={cKey}&guid={guid}&charge=1&encryptVer=5.4&lnk={vid}'.format(
                    vid=vid, appver=appver, filename=self._getfilename(lnk, format, idx),
                    format=format, cKey=cKey, guid=guid, platform=platform, lnk=lnk)
                if 'extractor_proxy' in kwargs and kwargs['extractor_proxy']:
                    set_proxy(parse_host(kwargs['extractor_proxy']))
                    part_info = get_html(key_api)
                    unset_proxy()
                else:
                    part_info = get_html(key_api)
                key_json = json.loads(match1(part_info, r'QZOutputJson=(.*)')[:-1])
                return 'key' in key_json and key_json['key']

            def __getitem__(self, key):
                if key == 'src' and 'src' not in self:
                    self['src'] = []
                    for idx in range(1, vi0['cl']['fc'] + 1) or [1]:
                        vkey = self._getvkey(vid, self.stream_id, idx)
                        if vkey:
                            url = '{prefix}/{filename}?vkey={vkey}'.format(prefix=url_prefix, filename=self._getfilename(lnk=lnk, stream_id=self.stream_id, idx=idx), vkey=vkey)
                            self['src'].append(url)
                    return self['src']
                else:
                    return dict.__getitem__(self, key)

        for f in fi:
            # urls = ['{prefix}/{vid}.p{format1000}.{idx}.mp4?vkey={vkey}'.format(prefix=url_prefix, vid=vid, format1000=f['id']%1000, idx=idx, vkey=self._getvkey(vid, f['id'], idx)) for idx in range(1, vi0['cl']['fc']+1)]

            # print(vi0['ul']['ui'])
            # vkey = self._getvkey(vid, f['id'], 1)
            # for ui in vi0['ul']['ui']:
            #     test = '{prefix}/{vid}.p{format1000}.1.mp4?vkey={vkey}'.format(prefix=ui['url'], vid=vid, format1000=f['id']%1000, vkey=vkey)
            #     print(test)

            self.streams[f['name']] = LazyDict(
                video_profile=f['cname'],
                size=f['fs'],
                container='mp4',
                stream_id=f['id'],
            )


site = QQ()


def qq_download(url, output_dir='.', merge=True, info_only=False, **kwargs):
    """"""
    if 'live.qq.com' in url:
        qieDownload(url, output_dir=output_dir, merge=merge, info_only=info_only)
        return

    if 'mp.weixin.qq.com/s?' in url:
        content = get_html(url)
        vids = matchall(content, [r'src=".+\bvid=(\w+).+"'])
        for vid in vids:
            site.download_by_vid(vid=vid, output_dir=output_dir, merge=merge, info_only=info_only, **kwargs)
        return

    # do redirect
    if 'v.qq.com/page' in url:
        # for URLs like this:
        # http://v.qq.com/page/k/9/7/k0194pwgw97.html
        url = get_location(url)

    if 'kuaibao.qq.com' in url or re.match(r'http://daxue.qq.com/content/content/id/\d+', url):
        content = get_html(url)
        vid = match1(content, r'vid\s*=\s*"\s*([^"]+)"')
        # title = match1(content, r'title">([^"]+)</p>')
        # title = title.strip() if title else vid
    elif 'iframe/player.html' in url:
        vid = match1(url, r'\bvid=(\w+)')
        # for embedded URLs; don't know what the title is
        # title = vid
    else:
        content = get_html(url)
        vid = parse_qs(urlparse(url).query).get(
            'vid')  # for links specified vid  like http://v.qq.com/cover/p/ps6mnfqyrfo7es3.html?vid=q0181hpdvo5
        vid = vid[0] if vid else match1(content, r'vid"*\s*:\s*"\s*([^"]+)"')  # general fallback
        # title = match1(content, r'<a.*?id\s*=\s*"%s".*?title\s*=\s*"(.+?)".*?>' % vid)
        # title = match1(content, r'title">([^"]+)</p>') if not title else title
        # title = match1(content, r'"title":"([^"]+)"') if not title else title
        # title = vid if not title else title  # general fallback

    site.download_by_vid(vid=vid, output_dir=output_dir, merge=merge, info_only=info_only, **kwargs)


qq_download_by_vid = site.download_by_vid
site_info = "QQ.com"
download = qq_download
download_playlist = playlist_not_supported('qq')
