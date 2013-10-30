#!/usr/bin/env python

# Original code from:
# http://xiaoxia.org/2011/03/26/using-python-to-write-a-local-sogou-proxy-server-procedures/

from . import log

from http.client import HTTPResponse
from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
from threading import Thread
import random, socket, struct, sys, time

def sogou_proxy_server(
    host=("0.0.0.0", 0),
    network_env='CERNET',
    ostream=sys.stderr):
    """Returns a Sogou proxy server object.
    """

    x_sogou_auth = '9CD285F1E7ADB0BD403C22AD1D545F40/30/853edc6d49ba4e27'
    proxy_host = 'h0.cnc.bj.ie.sogou.com'
    proxy_port = 80

    def sogou_hash(t, host):
        s = (t + host + 'SogouExplorerProxy').encode('ascii')
        code = len(s)
        dwords = int(len(s) / 4)
        rest = len(s) % 4
        v = struct.unpack(str(dwords) + 'i' + str(rest) + 's', s)
        for vv in v:
            if type(vv) != bytes:
                a = (vv & 0xFFFF)
                b = (vv >> 16)
                code += a
                code = code ^ (((code << 5) ^ b) << 0xb)
                # To avoid overflows
                code &= 0xffffffff
                code += code >> 0xb
        if rest == 3:
            code += s[len(s) - 2] * 256 + s[len(s) - 3]
            code = code ^ ((code ^ (s[len(s) - 1]) * 4) << 0x10)
            code &= 0xffffffff
            code += code >> 0xb
        elif rest == 2:
            code += (s[len(s) - 1]) * 256 + (s[len(s) - 2])
            code ^= code << 0xb
            code &= 0xffffffff
            code += code >> 0x11
        elif rest == 1:
            code += s[len(s) - 1]
            code ^= code << 0xa
            code &= 0xffffffff
            code += code >> 0x1
        code ^= code * 8
        code &= 0xffffffff
        code += code >> 5
        code ^= code << 4
        code = code & 0xffffffff
        code += code >> 0x11
        code ^= code << 0x19
        code = code & 0xffffffff
        code += code >> 6
        code = code & 0xffffffff
        return hex(code)[2:].rstrip('L').zfill(8)

    class Handler(BaseHTTPRequestHandler):
        _socket = None
        def do_proxy(self):
            try:
                if self._socket is None:
                    self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    self._socket.connect((proxy_host, proxy_port))
                self._socket.send(self.requestline.encode('ascii') + b'\r\n')
                log.d(self.requestline, ostream)

                # Add Sogou Verification Tags
                self.headers['X-Sogou-Auth'] = x_sogou_auth
                t = hex(int(time.time()))[2:].rstrip('L').zfill(8)
                self.headers['X-Sogou-Tag'] = sogou_hash(t, self.headers['Host'])
                self.headers['X-Sogou-Timestamp'] = t
                self._socket.send(str(self.headers).encode('ascii') + b'\r\n')

                # Send POST data
                if self.command == 'POST':
                    self._socket.send(self.rfile.read(int(self.headers['Content-Length'])))
                response = HTTPResponse(self._socket, method=self.command)
                response.begin()

                # Response
                status = 'HTTP/1.1 %s %s' % (response.status, response.reason)
                self.wfile.write(status.encode('ascii') + b'\r\n')
                h = ''
                for hh, vv in response.getheaders():
                    if hh.upper() != 'TRANSFER-ENCODING':
                        h += hh + ': ' + vv + '\r\n'
                self.wfile.write(h.encode('ascii') + b'\r\n')
                while True:
                    response_data = response.read(8192)
                    if len(response_data) == 0:
                        break
                    self.wfile.write(response_data)

            except socket.error:
                log.e('Socket error for ' + self.requestline, ostream)

        def do_POST(self):
            self.do_proxy()

        def do_GET(self):
            self.do_proxy()

    class ThreadingHTTPServer(ThreadingMixIn, HTTPServer):
        pass

    # Server starts
    log.printlog('Sogou Proxy Mini-Server', color='bold-green', ostream=ostream)

    try:
        server = ThreadingHTTPServer(host, Handler)
    except Exception as ex:
        log.wtf("Socket error: %s" % ex, ostream)
        exit(1)
    host = server.server_address

    if network_env.upper() == 'CERNET':
        proxy_host = 'h%s.edu.bj.ie.sogou.com' % random.randint(0, 10)
    elif network_env.upper() == 'CTCNET':
        proxy_host = 'h%s.ctc.bj.ie.sogou.com' % random.randint(0, 3)
    elif network_env.upper() == 'CNCNET':
        proxy_host = 'h%s.cnc.bj.ie.sogou.com' % random.randint(0, 3)
    elif network_env.upper() == 'DXT':
        proxy_host = 'h%s.dxt.bj.ie.sogou.com' % random.randint(0, 10)
    else:
        proxy_host = 'h%s.edu.bj.ie.sogou.com' % random.randint(0, 10)

    log.i('Remote host: %s' % log.underlined(proxy_host), ostream)
    log.i('Proxy server running on %s' %
        log.underlined("%s:%s" % host), ostream)

    return server
