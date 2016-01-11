#!/usr/bin/env python

import subprocess
from flask import Flask, request
app = Flask(__name__)

# 使用vlc进行播放
@app.route('/play/')
def hello_world():
    url = request.args.get('url')
    if url!=None:
        print('url is::'+url)
        cmd = 'python3 you-get -p vlc ' + url
        subprocess.Popen(cmd, shell=True)
    return 'End'

if __name__ == '__main__':
    app.run(debug=True)
