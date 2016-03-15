#!/usr/bin/env python

import json
import os
import re
import math
import traceback
import urllib.parse as urlparse

from ..common import *

__all__ = ['huaban_download']

site_info = '花瓣 (Huaban)'

LIMIT = 100


class Board:
    def __init__(self, title, pins):
        self.title = title
        self.pins = pins
        self.pin_count = len(pins)


class Pin:
    host = 'http://img.hb.aicdn.com/'

    def __init__(self, pin_json):
        img_file = pin_json['file']
        self.id = str(pin_json['pin_id'])
        self.url = urlparse.urljoin(self.host, img_file['key'])
        self.ext = img_file['type'].split('/')[-1]


def construct_url(url, **params):
    param_str = urlparse.urlencode(params)
    return url + '?' + param_str


def extract_json_data(url, **params):
    url = construct_url(url, **params)
    html = get_content(url, headers=fake_headers)
    json_string = match1(html, r'app.page\["board"\] = (.*?});')
    json_data = json.loads(json_string)
    return json_data


def extract_board_data(url):
    json_data = extract_json_data(url, limit=LIMIT)
    pin_list = json_data['pins']
    title = json_data['title']
    pin_count = json_data['pin_count']
    pin_count -= len(pin_list)

    while pin_count > 0:
        json_data = extract_json_data(url, max=pin_list[-1]['pin_id'],
                                      limit=LIMIT)
        pins = json_data['pins']
        pin_list += pins
        pin_count -= len(pins)

    return Board(title, list(map(Pin, pin_list)))


def huaban_download_board(url, output_dir, **kwargs):
    kwargs['merge'] = False
    board = extract_board_data(url)
    output_dir = os.path.join(output_dir, board.title)
    print_info(site_info, board.title, 'jpg', float('Inf'))
    for pin in board.pins:
        download_urls([pin.url], pin.id, pin.ext, float('Inf'),
                      output_dir=output_dir, faker=True, **kwargs)


def huaban_download(url, output_dir='.', **kwargs):
    if re.match(r'http://huaban\.com/boards/\d+/', url):
        huaban_download_board(url, output_dir, **kwargs)
    else:
        print('Only board (画板) pages are supported currently')
        print('ex: http://huaban.com/boards/12345678/')


download = huaban_download
download_playlist = playlist_not_supported("huaban")
