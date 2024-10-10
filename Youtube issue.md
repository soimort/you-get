Traceback (most recent call last):
  File "<frozen runpy>", line 198, in _run_module_as_main
  File "<frozen runpy>", line 88, in _run_code
  File "C:\Users\buyan\AppData\Local\Programs\Python\Python312\Scripts\you-get.exe\__main__.py", line 7, in <module>
  File "C:\Users\buyan\AppData\Local\Programs\Python\Python312\Lib\site-packages\you_get\__main__.py", line 92, in main
    main(**kwargs)
  File "C:\Users\buyan\AppData\Local\Programs\Python\Python312\Lib\site-packages\you_get\common.py", line 1883, in main
    script_main(any_download, any_download_playlist, **kwargs)
  File "C:\Users\buyan\AppData\Local\Programs\Python\Python312\Lib\site-packages\you_get\common.py", line 1772, in script_main
    download_main(
  File "C:\Users\buyan\AppData\Local\Programs\Python\Python312\Lib\site-packages\you_get\common.py", line 1386, in download_main
    download(url, **kwargs)
  File "C:\Users\buyan\AppData\Local\Programs\Python\Python312\Lib\site-packages\you_get\common.py", line 1874, in any_download
    m.download(url, **kwargs)
  File "C:\Users\buyan\AppData\Local\Programs\Python\Python312\Lib\site-packages\you_get\extractor.py", line 48, in download_by_url
    self.prepare(**kwargs)
  File "C:\Users\buyan\AppData\Local\Programs\Python\Python312\Lib\site-packages\you_get\extractors\youtube.py", line 252, in prepare
    url = self.__class__.dethrottle(self.js, url)
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\buyan\AppData\Local\Programs\Python\Python312\Lib\site-packages\you_get\extractors\youtube.py", line 91, in dethrottle
    n = n_to_n(js, qs['n'][0])
        ^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\buyan\AppData\Local\Programs\Python\Python312\Lib\site-packages\you_get\extractors\youtube.py", line 85, in n_to_n
    f1def = match1(js, r'\W%s=(function\(\w+\).+?\)});' % re.escape(f1))
                                                          ^^^^^^^^^^^^^
  File "C:\Users\buyan\AppData\Local\Programs\Python\Python312\Lib\re\__init__.py", line 262, in escape
    pattern = str(pattern, 'latin1')
              ^^^^^^^^^^^^^^^^^^^^^^
TypeError: decoding to str: need a bytes-like object, NoneType found

