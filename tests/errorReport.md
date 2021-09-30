just a regular search
```
D:\download>you-get "hotdog cooking" --debug
[DEBUG] get_content: https://www.google.com/search?tbm=vid&q=hotdog%20cooking
you-get: version 0.4.1545, a tiny downloader that scrapes the web.
you-get: Namespace(version=False, help=False, info=False, url=False, json=False, no_merge=False, no_caption=False, force=False, skip_existing_file_size_check=False, format=None, output_filename=None, output_dir='.', player=None, cookies=None, timeout=600, debug=True, input_file=None, password=None, playlist=False, first=None, last=None, size=None, auto_rename=False, insecure=False, http_proxy=None, extractor_proxy=None, no_proxy=False, socks_proxy=None, stream=None, itag=None, URL=['hotdog cooking'])
Traceback (most recent call last):
  File "C:\Python39\lib\site-packages\you_get\common.py", line 1786, in url_to_module
    assert video_host and video_url
AssertionError

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "C:\Python39\lib\runpy.py", line 197, in _run_module_as_main
    return _run_code(code, main_globals, None,
  File "C:\Python39\lib\runpy.py", line 87, in _run_code
    exec(code, run_globals)
  File "C:\Python39\Scripts\you-get.exe\__main__.py", line 7, in <module>
  File "C:\Python39\lib\site-packages\you_get\__main__.py", line 92, in main
    main(**kwargs)
  File "C:\Python39\lib\site-packages\you_get\common.py", line 1831, in main
    script_main(any_download, any_download_playlist, **kwargs)
  File "C:\Python39\lib\site-packages\you_get\common.py", line 1713, in script_main
    download_main(
  File "C:\Python39\lib\site-packages\you_get\common.py", line 1345, in download_main
    download(url, **kwargs)
  File "C:\Python39\lib\site-packages\you_get\common.py", line 1821, in any_download
    m, url = url_to_module(url)
  File "C:\Python39\lib\site-packages\you_get\common.py", line 1788, in url_to_module
    url = google_search(url)
  File "C:\Python39\lib\site-packages\you_get\common.py", line 1779, in google_search
    return(videos[0][0])
IndexError: list index out of range
Google Videos search:
Best matched result:

D:\download>
```
