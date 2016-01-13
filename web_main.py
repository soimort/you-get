#!/usr/bin/env python

import os, sys
from multiprocessing import Process
from flask import Flask, request

app = Flask(__name__)

_srcdir = 'src/'
_filepath = os.path.dirname(sys.argv[0])
sys.path.insert(1, os.path.join(_filepath, _srcdir))

from you_get import common

def you_get_down(urls):
    common.download_main(common.any_download, common.any_download_playlist, urls, False,
                         output_dir='tmp/', merge=True, info_only=False, json_output=False, caption=True)

def you_get_play(player, urls):
    common.player = 'vlc'
    common.download_main(common.any_download, common.any_download_playlist, urls, False,
                         output_dir='tmp', merge=True, info_only=False, json_output=False, caption=True)

@app.route('/action/')
def action():
    type = request.args.get('type')
    url = request.args.get('url')
    if url==None:
        return 'Fail'
    print('url is::'+url)
    p = None
    if type == 'play':
        p = Process(target=you_get_play, args=('vlc', [url],))
    elif type == 'download':
        p = Process(target=you_get_down, args=([url],))
    if p != None:
        p.start()
    return 'Success'

if sys.version_info.major == 3:
    if __name__ == '__main__':
        app.run(debug=True)
else:
    print("Need python3")
