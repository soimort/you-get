#!/usr/bin/env python

import json
import os
import sys
from urllib import request, parse, error
import time

fake_headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',  # noqa
    'Accept-Charset': 'UTF-8,*;q=0.5',
    'Accept-Encoding': 'gzip,deflate,sdch',
    'Accept-Language': 'en-US,en;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.74 Safari/537.36 Edg/79.0.309.43',  # noqa
}

class Aria2cDownloader:

    def __init__(self, rpc, secret, options={}, error_logger=print):
        base = {
                'jsonrpc':'2.0',
                'id':'you-get',
                'params':[]
                }

        if secret is not None:
            base['params'].append('token:%s' % secret)

        self.base = json.dumps(base)
        self.options = json.dumps(options)
        self.rpc = rpc
        self.error_logger = error_logger
        self.bar = None

    def log_error(self, msg):
        if self.bar:
            sys.stderr.write('\n')
            self.bar = None
        self.error_logger(msg)

    def request(self, base):
        req = json.dumps(base).encode('utf-8')
        try:
            r = request.urlopen(self.rpc, req)
            return json.loads(r.read().decode('utf-8'))
        except error.HTTPError as e:
            self.log_error('Error connecting aria2c via %s' % self.rpc)
            rep = json.loads(e.read())
            self.log_error(rep["error"]["message"])
            exit(1)

    def download(self, urls, filepath, bar, refer=None, is_part=False,
            faker=False, headers=None, timeout=None, **kwargs):
        self.bar = bar
        download_base = json.loads(self.base)
        download_options = json.loads(self.options)

        if type(urls) is not list:
            urls = [urls]

        download_options['out'] = os.path.basename(filepath)
        download_options['dir'] = os.path.abspath(os.path.dirname(filepath))

        if refer is not None:
            download_options['referer'] = refer

        if faker:
            headers = fake_headers

        if headers:
            download_options['header'] = \
                [ '%s: %s' % (k, v) for (k, v) in headers.items() ]

        download_base['method'] = 'aria2.addUri'
        download_base['params'] += [urls, download_options]

        result = self.request(download_base)
        gid = result['result']

        received = 0
        while True:
            time.sleep(1)
            status = self.tell_status(gid)
            s = status['status']
            if s == 'removed':
                self.log_error('download removed')
                exit(1)
            if s == 'error':
                self.log_error('download failed')
                exit(1)
            if s == 'complete':
                bar.done()
                break
            if bar:
                completed = int(status['completedLength'])
                delta = completed - received
                received = completed
                bar.update_received(delta)
        self.bar = None

    def tell_status(self, gid):

        base = json.loads(self.base)
        options = json.loads(self.options)

        base['params'] += [gid, ['status', 'completedLength']]
        base['method'] = 'aria2.tellStatus'

        return self.request(base)['result']
