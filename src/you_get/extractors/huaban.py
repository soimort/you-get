#!/usr/bin/env python

import json
import os
import re
import traceback
import urllib.parse as urlparse

from ..common import *

__all__ = ['huaban_download']

site_info = '花瓣 (Huaban)'

LIMIT = 100


class EnhancedPiecesProgressBar(PiecesProgressBar):
    BAR_LEN = 40

    def update(self):
        self.displayed = True
        bar = '{0:>5}%[{1}] {2}/{3}'.format(
            '', '=' * self.done_bar + '-' * self.todo_bar,
            self.current_piece, self.total_pieces)
        sys.stdout.write('\r' + bar)
        sys.stdout.flush()

    @property
    def done_bar(self):
        return self.BAR_LEN // self.total_pieces * self.current_piece

    @property
    def todo_bar(self):
        return self.BAR_LEN - self.done_bar


class Board:
    def __init__(self, title, pins):
        self.title = title
        self.pins = pins
        self.pin_count = len(pins)


class Pin:
    host = 'http://img.hb.aicdn.com/'

    def __init__(self, pin_json):
        img_file = pin_json['file']
        self.key = img_file['key']
        self.url = urlparse.urljoin(self.host, self.key)
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


def get_num_len(num):
    return len(str(num))


def huaban_download_board(url, output_dir, **kwargs):
    board = extract_board_data(url)
    output_dir = os.path.join(output_dir, board.title)
    bar = EnhancedPiecesProgressBar(float('Inf'), board.pin_count)

    print("Site:      ", site_info)
    print("Title:     ", board.title)
    print()

    if dry_run:
        urls = '\n'.join(map(lambda p: p.url, board.pins))
        print('Real URLs:\n{}'.format(urls))
        return

    print('Downloading {} images in {} ...'.format(board.pin_count,
                                                   board.title))
    try:
        bar.update()
        name_len = get_num_len(board.pin_count)
        for i, pin in enumerate(board.pins):
            filename = '{0}[{1}].{2}'.format(board.title,
                                             str(i).zfill(name_len), pin.ext)
            filepath = os.path.join(output_dir, filename)
            bar.update_piece(i + 1)
            url_save(pin.url, filepath, bar, is_part=True, faker=True)
        bar.done()
    except KeyboardInterrupt:
        pass
    except:
        traceback.print_exception(*sys.exc_info())


def huaban_download(url, output_dir='.', **kwargs):
    if re.match(r'http://huaban\.com/boards/\d+/', url):
        huaban_download_board(url, output_dir, **kwargs)
    else:
        print('Only board (画板) pages are supported currently')
        print('ex: http://huaban.com/boards/12345678/')


download = huaban_download
download_playlist = playlist_not_supported("huaban")
