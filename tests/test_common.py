#!/usr/bin/env python
import http.server
import socketserver
import tempfile
import threading
import unittest

from you_get.common import *


class TestCommon(unittest.TestCase):
    
    def test_match1(self):
        self.assertEqual(match1('http://youtu.be/1234567890A', r'youtu.be/([^/]+)'), '1234567890A')
        self.assertEqual(match1('http://youtu.be/1234567890A', r'youtu.be/([^/]+)', r'youtu.(\w+)'), ['1234567890A', 'be'])


class TestDownloadUrlWithoutContentLength(unittest.TestCase):
    def setUp(self):
        self.server = ChunkedTestServer()
        self.port = self.server.start()

    def tearDown(self):
        self.server.stop()

    def test_server_response(self):
        response = request.urlopen(f'http://localhost:{self.port}')
        self.assertEqual(response.status, 200)
        self.assertNotIn('Content-Length', response.headers)

        expected_data = b'First chunk of data\nSecond chunk of data\nLast chunk of data'
        self.assertEqual(response.read(), expected_data)

    def test_url_save(self):
        with tempfile.NamedTemporaryFile() as temp_file:
            temp_path = temp_file.name

        try:
            url_save([f'http://localhost:{self.port}'], temp_path, None)

            with open(temp_path, "r") as f:
                expected_data = 'First chunk of data\nSecond chunk of data\nLast chunk of data'
                self.assertEqual(f.read(), expected_data)
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)


class ChunkedHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Transfer-Encoding', 'chunked')
        self.end_headers()

        # Send data in chunks
        chunks = [b"First chunk of data\n",
                  b"Second chunk of data\n",
                  b"Last chunk of data"]

        for chunk in chunks:
            self.wfile.write(f"{len(chunk):x}\r\n".encode())
            self.wfile.write(chunk)
            self.wfile.write(b"\r\n")

        # Write the final chunk (zero-length chunk to indicate the end)
        self.wfile.write(b"0\r\n\r\n")


class ChunkedTestServer:
    def __init__(self, port=0):
        self.port = port
        self.server = socketserver.TCPServer(('localhost', port), ChunkedHTTPRequestHandler)
        self.server_thread = None

    def start(self):
        self.server_thread = threading.Thread(target=self.server.serve_forever)
        self.server_thread.daemon = True
        self.server_thread.start()
        self.port = self.server.server_address[1]
        return self.port

    def stop(self):
        self.server.shutdown()
        self.server.server_close()
        self.server_thread.join()
