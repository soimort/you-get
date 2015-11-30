#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'johnx'
__date__ = '6/18/14 10:56 AM'


import time
import urllib
import base64
import pdb
#import requests


def wget(url, **kwargs):
    kwargs.setdefault('timeout', 30)
    headers = DEFAULT_HEADERS.copy()
    headers.update(kwargs.get('headers', {}))
    kwargs['headers'] = headers

    return requests.get(url, **kwargs).content


def wget2(url, type_=None, **kwargs):
    content = wget(url)
    if type_ == 'json':
        return json.loads(content, **kwargs)

    return content


def trans_e(a, c):
    b = range(256)
    f = 0
    result = ''
    h = 0
    while h < 256:
        f = (f + b[h] + ord(a[h % len(a)])) % 256
        b[h], b[f] = b[f], b[h]
        h += 1

    q = f = h = 0
    while q < len(c):
        h = (h + 1) % 256
        f = (f + b[h]) % 256
        b[h], b[f] = b[f], b[h]
        result += chr(ord(c[q]) ^ b[(b[h] + b[f]) % 256])
        q += 1

    return result


def trans_f(a, c):
    """
    :argument a: list
    :param c:
    :return:
    """
    b = []
    for f in range(len(a)):
        i = ord(a[f][0]) - 97 if "a" <= a[f] <= "z" else int(a[f]) + 26
        e = 0
        while e < 36:
            if c[e] == i:
                i = e
                break

            e += 1

        v = i - 26 if i > 25 else chr(i + 97)
        b.append(str(v))

    return ''.join(b)


# array_1 = [
#     19, 1, 4, 7, 30, 14, 28, 8, 24, 17, 6, 35,
#     34, 16, 9, 10, 13, 22, 32, 29, 31, 21, 18,
#     3, 2, 23, 25, 27, 11, 20, 5, 15, 12, 0, 33, 26
# ]
# array_2 = [
#     19, 1, 4, 7, 30, 14, 28, 8, 24, 17,
#     6, 35, 34, 16, 9, 10, 13, 22, 32, 29,
#     31, 21, 18, 3, 2, 23, 25, 27, 11, 20,
#     5, 15, 12, 0, 33, 26
# ]
# code_1 = 'b4eto0b4'
# code_2 = 'boa4poz1'
# f_code_1 = trans_f(code_1, array_1)
# f_code_2 = trans_f(code_2, array_2)
f_code_1 = 'becaf9be'
f_code_2 = 'bf7e5f01'


# print `trans_e(f_code_1, trans_na('NgXQTQ0fJr7d0vHA8OJxA4nz6xJs1wnJXx8='))`

def parse(seed, ):
    sl = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ/\:._-1234567890"
    seed = float(seed)
    while sl:
        seed = (seed * 211 + 30031) % 65536
        idx = int(seed / 65536 * len(sl))
        yield sl[idx]
        sl = sl[:idx] + sl[idx+1:]


def parse2(file_id, seed):
    mix = ''.join(parse(seed))
    return ''.join(mix[int(idx)] for idx in file_id[:-1].split('*'))


def calc_ep2(vid, ep):
    e_code = trans_e(f_code_1, base64.b64decode(ep))
    sid, token = e_code.split('_')
    new_ep = trans_e(f_code_2, '%s_%s_%s' % (sid, vid, token))
    return base64.b64encode(new_ep), token, sid


def test2(evid):
    pdb.set_trace()
    base_url = 'http://v.youku.com/player/getPlayList/VideoIDS/%s/Pf/4/ctype/12/ev/1'
    json = wget2(base_url % evid, 'json')
    data = json['data'][0]
    file_ids = data['streamfileids']
    seed = data['seed']
    video_id = data['videoid']
    for type_, file_id in file_ids.items():
        if type_ != 'mp4':
            continue

        if '*' in file_id:
            file_id = file_ids[type_] = parse2(file_id, seed)

#        print '%s: %s' % (type_, file_id)

        new_ep, token, sid = calc_ep2(video_id, data['ep'])
#        print new_ep, token, sid

        query = urllib.urlencode(dict(
            vid=video_id, ts=int(time.time()), keyframe=1, type=type_,
            ep=new_ep, oip=data['ip'], ctype=12, ev=1, token=token, sid=sid,
        ))
        url = 'http://pl.youku.com/playlist/m3u8?' + query
#        print
#        print url
#       print wget2(url)


test2('XNzI2MjY2MTAw')
