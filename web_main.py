#!/usr/bin/env python

import os, sys
from flask import Flask, request

app = Flask(__name__)

_srcdir = 'src/'
_filepath = os.path.dirname(sys.argv[0])
sys.path.insert(1, os.path.join(_filepath, _srcdir))

from you_get import common

# 使用vlc进行播放
@app.route('/play/')
def hello_world():
    url = request.args.get('url')
    if url!=None:
        print('url is::'+url)
        common.player = 'vlc'
        common.download_main(common.any_download, common.any_download_playlist, [url], False,
                             output_dir='.', merge=True, info_only=False, json_output=False, caption=True)
    return 'End'

if sys.version_info.major == 3:
    if __name__ == '__main__':
        app.run(debug=True)
else:
    print("Need python3")
