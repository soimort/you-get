import json
import unittest
from unittest.mock import MagicMock, patch
from urllib.error import HTTPError

from you_get.common import url_to_module
from you_get.extractors import alipay


class TestAlipay(unittest.TestCase):
    def response(self, status=200, headers=None, url='', body=b''):
        response = MagicMock()
        response.__enter__.return_value = response
        response.status = status
        response.headers = headers or {}
        response.geturl.return_value = url
        response.read.return_value = body
        return response

    def test_dispatch(self):
        for url in ('https://ur.lepudding.com/share', 'https://render.alipay.com/detail?contentId=ABC123'):
            module, resolved = url_to_module(url)
            self.assertIs(module, alipay)
            self.assertEqual(resolved, url)

    def test_content_id(self):
        for text in ('https://example.com/?contentId=ABC123&x=1',
                     'alipays://start?url=%2Fdetail%3FcontentId%3DABC123%26x%3D1',
                     'contentId%253DABC123'):
            self.assertEqual(alipay.content_id(text), 'ABC123')
        self.assertIsNone(alipay.content_id('https://example.com/no-video'))

    @patch.object(alipay, 'urlopen_with_retry')
    def test_resolve(self, open_url):
        open_url.return_value = self.response(url='https://example.com/?contentId=ABC123')
        self.assertEqual(alipay.resolve_content_id('https://ur.lepudding.com/share'), 'ABC123')
        open_url.return_value.__exit__.assert_called_once()
        open_url.return_value = self.response(body=b'contentId%3DABC123')
        self.assertEqual(alipay.resolve_content_id('https://ur.lepudding.com/share'), 'ABC123')
        open_url.return_value = self.response()
        with self.assertRaisesRegex(ValueError, 'could not find'):
            alipay.resolve_content_id('https://ur.lepudding.com/share')
        open_url.reset_mock()
        self.assertEqual(alipay.resolve_content_id('https://example.com/?contentId=ABC123'), 'ABC123')
        open_url.assert_not_called()

    @patch.object(alipay, 'post_content')
    def test_detail(self, post):
        post.return_value = json.dumps({'success': True, 'resultObj': {'data': [{'title': 'test', 'video': {'vid': 'https://cdn.example/video.mp4'}}]}})
        self.assertEqual(alipay.fetch_detail('ABC123')['title'], 'test')
        self.assertEqual(json.loads(post.call_args.kwargs['post_data_raw']), {'contentId': 'ABC123'})
        self.assertEqual(post.call_args.kwargs['headers']['x-webgw-appId'], '180020010001266490')
        for data in ({'success': False, 'errorMessage': 'gone'}, {'success': True},
                     {'success': True, 'resultObj': {'data': []}},
                     {'success': True, 'resultObj': {'data': [{'video': None}]}}, []):
            post.return_value = json.dumps(data)
            with self.assertRaises(ValueError):
                alipay.fetch_detail('ABC123')

    def test_candidates(self):
        candidates = list(alipay.stream_candidates('https://cdn.example/video/720P_h265?t=token&extra=value'))
        self.assertEqual(candidates[0], 'https://cdn.example/video/1080P_h265_EH?t=token&extra=value')
        self.assertEqual(list(alipay.stream_candidates('https://cdn.example/video.mp4')), ['https://cdn.example/video.mp4'])
        with self.assertRaises(ValueError):
            list(alipay.stream_candidates('file:///tmp/video.mp4'))

    @patch.object(alipay, 'urlopen_with_retry')
    def test_probe_fallback(self, open_url):
        open_url.side_effect = [HTTPError('', 404, 'missing', {}, None),
                                self.response(206, {'Content-Range': 'bytes 0-0/12345', 'Content-Length': '1'})]
        url, size = alipay.pick_stream('https://cdn.example/video/720P_h265?t=token')
        self.assertIn('/1080P_h265?', url)
        self.assertEqual(size, 12345)
        self.assertEqual(open_url.call_args.args[0].get_header('Range'), 'bytes=0-0')

    @patch.object(alipay, 'urlopen_with_retry')
    def test_original_and_missing_stream(self, open_url):
        open_url.return_value = self.response(200, {'Content-Length': '42'})
        self.assertEqual(alipay.pick_stream('https://cdn.example/video.mp4'), ('https://cdn.example/video.mp4', 42))
        open_url.return_value = self.response(206, {'Content-Length': '1'})
        with self.assertRaisesRegex(ValueError, 'no available'):
            alipay.pick_stream('https://cdn.example/video.mp4')

    @patch.object(alipay, 'download_urls')
    @patch.object(alipay, 'print_info')
    @patch.object(alipay, 'pick_stream', return_value=('https://cdn.example/video.mp4', 42))
    @patch.object(alipay, 'fetch_detail', return_value={'title': '', 'video': {'vid': 'https://cdn.example/video.mp4'}})
    def test_download(self, detail, pick, info, download):
        alipay.download('https://example.com/?contentId=ABC123', info_only=True)
        download.assert_not_called()
        info.assert_called_with('Alipay (支付宝)', 'ABC123', 'mp4', 42)
        alipay.download('https://example.com/?contentId=ABC123', output_dir='/tmp/out', merge=False)
        download.assert_called_once_with(['https://cdn.example/video.mp4'], 'ABC123', 'mp4', 42, output_dir='/tmp/out', merge=False)


if __name__ == '__main__':
    unittest.main()
