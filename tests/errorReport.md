# error report

## The command was:

```bash
you-get -a -l --debug https://www.bilibili.com/bangumi/play/ss25210/?from=search&seid=3510815631300967887&spm_id_from=333.337.0.0
```
## error log says:

When scraping videos from `www.bilibili.com` in command line at terminal, an unknown error occured, whose log was as follows:

```bash
[DEBUG] get_content: https://www.bilibili.com/bangumi/play/ss25210/?from=search
you-get: Extracting 1 of 24 videos ...
[DEBUG] get_content: https://www.bilibili.com/bangumi/play/ep239607/
[DEBUG] get_content: https://api.bilibili.com/pgc/player/web/playurl?avid=27985827&cid=48346081&qn=0&type=&otype=json&ep_id=239607&fnver=0&fnval=16
[DEBUG] get_content: https://api.bilibili.com/pgc/player/web/playurl?avid=27985827&cid=48346081&qn=120&type=&otype=json&ep_id=239607&fnver=0&fnval=8
[DEBUG] get_content: https://api.bilibili.com/pgc/player/web/playurl?avid=27985827&cid=48346081&qn=112&type=&otype=json&ep_id=239607&fnver=0&fnval=8
[DEBUG] get_content: https://api.bilibili.com/pgc/player/web/playurl?avid=27985827&cid=48346081&qn=80&type=&otype=json&ep_id=239607&fnver=0&fnval=8
[DEBUG] get_content: https://api.bilibili.com/pgc/player/web/playurl?avid=27985827&cid=48346081&qn=64&type=&otype=json&ep_id=239607&fnver=0&fnval=8
[DEBUG] get_content: https://api.bilibili.com/pgc/player/web/playurl?avid=27985827&cid=48346081&qn=16&type=&otype=json&ep_id=239607&fnver=0&fnval=8
[DEBUG] get_content: https://api.bilibili.com/pgc/player/web/playurl?avid=27985827&cid=48346081&qn=120&type=&otype=json&ep_id=239607&fnver=0&fnval=16
[DEBUG] get_content: https://api.bilibili.com/pgc/player/web/playurl?avid=27985827&cid=48346081&qn=112&type=&otype=json&ep_id=239607&fnver=0&fnval=16
[DEBUG] get_content: https://api.bilibili.com/pgc/player/web/playurl?avid=27985827&cid=48346081&qn=80&type=&otype=json&ep_id=239607&fnver=0&fnval=16
[DEBUG] get_content: https://api.bilibili.com/pgc/player/web/playurl?avid=27985827&cid=48346081&qn=64&type=&otype=json&ep_id=239607&fnver=0&fnval=16
[DEBUG] get_content: https://api.bilibili.com/pgc/player/web/playurl?avid=27985827&cid=48346081&qn=16&type=&otype=json&ep_id=239607&fnver=0&fnval=16
you-get: version 0.4.1545, a tiny downloader that scrapes the web.
you-get: Namespace(version=False, help=False, info=False, url=False, json=False, no_merge=False, no_caption=False, force=False, skip_existing_file_size_check=False, format=None, output_filename=None, output_dir='.', player=None, cookies=None, timeout=600, debug=True, input_file=None, password=None, playlist=True, first=None, last=None, size=None, auto_rename=True, insecure=False, http_proxy=None, extractor_proxy=None, no_proxy=False, socks_proxy=None, stream=None, itag=None, URL=['https://www.bilibili.com/bangumi/play/ss25210/?from=search'])
Traceback (most recent call last):
File "/usr/lib/python3.9/urllib/request.py", line 1346, in do_open
h.request(req.get_method(), req.selector, req.data, headers,
File "/usr/lib/python3.9/http/client.py", line 1257, in request
self._send_request(method, url, body, headers, encode_chunked)
File "/usr/lib/python3.9/http/client.py", line 1303, in _send_request
self.endheaders(body, encode_chunked=encode_chunked)
File "/usr/lib/python3.9/http/client.py", line 1252, in endheaders
self._send_output(message_body, encode_chunked=encode_chunked)
File "/usr/lib/python3.9/http/client.py", line 1012, in _send_output
self.send(msg)
File "/usr/lib/python3.9/http/client.py", line 952, in send
self.connect()
File "/usr/lib/python3.9/http/client.py", line 1419, in connect
super().connect()
File "/usr/lib/python3.9/http/client.py", line 923, in connect
self.sock = self._create_connection(
File "/usr/lib/python3.9/socket.py", line 822, in create_connection
for res in getaddrinfo(host, port, 0, SOCK_STREAM):
File "/usr/lib/python3.9/socket.py", line 953, in getaddrinfo
for res in _socket.getaddrinfo(host, port, family, type, proto, flags):
socket.gaierror: [Errno -2] Name or service not known

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
File "/usr/bin/you-get", line 33, in <module>
sys.exit(load_entry_point('you-get==0.4.1545', 'console_scripts', 'you-get')())
File "/usr/lib/python3.9/site-packages/you_get/__main__.py", line 92, in main
main(**kwargs)
File "/usr/lib/python3.9/site-packages/you_get/common.py", line 1831, in main
script_main(any_download, any_download_playlist, **kwargs)
File "/usr/lib/python3.9/site-packages/you_get/common.py", line 1713, in script_main
download_main(
File "/usr/lib/python3.9/site-packages/you_get/common.py", line 1343, in download_main
download_playlist(url, **kwargs)
File "/usr/lib/python3.9/site-packages/you_get/common.py", line 1827, in any_download_playlist
m.download_playlist(url, **kwargs)
File "/usr/lib/python3.9/site-packages/you_get/extractors/bilibili.py", line 683, in download_playlist_by_url
self.__class__().download_by_url(epurl, **kwargs)
File "/usr/lib/python3.9/site-packages/you_get/extractor.py", line 48, in download_by_url
self.prepare(**kwargs)
File "/usr/lib/python3.9/site-packages/you_get/extractors/bilibili.py", line 363, in prepare
size = url_size(baseurl, headers=self.bilibili_headers(referer=self.url))
File "/usr/lib/python3.9/site-packages/you_get/common.py", line 533, in url_size
response = urlopen_with_retry(request.Request(url, headers=headers))
File "/usr/lib/python3.9/site-packages/you_get/common.py", line 408, in urlopen_with_retry
return request.urlopen(*args, **kwargs)
File "/usr/lib/python3.9/urllib/request.py", line 214, in urlopen
return opener.open(url, data, timeout)
File "/usr/lib/python3.9/urllib/request.py", line 517, in open
response = self._open(req, data)
File "/usr/lib/python3.9/urllib/request.py", line 534, in _open
result = self._call_chain(self.handle_open, protocol, protocol +
File "/usr/lib/python3.9/urllib/request.py", line 494, in _call_chain
result = func(*args)
File "/usr/lib/python3.9/urllib/request.py", line 1389, in https_open
return self.do_open(http.client.HTTPSConnection, req,
File "/usr/lib/python3.9/urllib/request.py", line 1349, in do_open
raise URLError(err)
urllib.error.URLError: <urlopen error [Errno -2] Name or service not known>
^C
[1]-  退出 1                you-get -a -l --debug https://www.bilibili.com/bangumi/play/ss25210/?from=search
[2]+  已完成               seid=3510815631300967887
```
