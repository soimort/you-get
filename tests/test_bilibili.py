#!/usr/bin/env python

import unittest
from unittest.mock import patch
import os
import time
from http import cookiejar

from you_get.util import log, term
from you_get.extractors import bilibili


def load_cookies(cookiefile):
    cookies = None
    if cookiefile.endswith('.txt'):
        # MozillaCookieJar treats prefix '#HttpOnly_' as comments incorrectly!
        # do not use its load()
        # see also:
        #   - https://docs.python.org/3/library/http.cookiejar.html#http.cookiejar.MozillaCookieJar
        #   - https://github.com/python/cpython/blob/4b219ce/Lib/http/cookiejar.py#L2014
        #   - https://curl.haxx.se/libcurl/c/CURLOPT_COOKIELIST.html#EXAMPLE
        # cookies = cookiejar.MozillaCookieJar(cookiefile)
        # cookies.load()
        from http.cookiejar import Cookie
        cookies = cookiejar.MozillaCookieJar()
        now = time.time()
        ignore_discard, ignore_expires = False, False
        with open(cookiefile, 'r', encoding='utf-8') as f:
            for line in f:
                # last field may be absent, so keep any trailing tab
                if line.endswith("\n"): line = line[:-1]

                # skip comments and blank lines XXX what is $ for?
                if (line.strip().startswith(("#", "$")) or
                        line.strip() == ""):
                    if not line.strip().startswith('#HttpOnly_'):  # skip for #HttpOnly_
                        continue

                domain, domain_specified, path, secure, expires, name, value = \
                    line.split("\t")
                secure = (secure == "TRUE")
                domain_specified = (domain_specified == "TRUE")
                if name == "":
                    # cookies.txt regards 'Set-Cookie: foo' as a cookie
                    # with no name, whereas http.cookiejar regards it as a
                    # cookie with no value.
                    name = value
                    value = None

                initial_dot = domain.startswith(".")
                if not line.strip().startswith('#HttpOnly_'):  # skip for #HttpOnly_
                    assert domain_specified == initial_dot

                discard = False
                if expires == "":
                    expires = None
                    discard = True

                # assume path_specified is false
                c = Cookie(0, name, value,
                           None, False,
                           domain, domain_specified, initial_dot,
                           path, False,
                           secure,
                           expires,
                           discard,
                           None,
                           None,
                           {})
                if not ignore_discard and c.discard:
                    continue
                if not ignore_expires and c.is_expired(now):
                    continue
                cookies.set_cookie(c)

    elif cookiefile.endswith(('.sqlite', '.sqlite3')):
        import sqlite3, shutil, tempfile
        temp_dir = tempfile.gettempdir()
        temp_cookiefile = os.path.join(temp_dir, 'temp_cookiefile.sqlite')
        shutil.copy2(cookiefile, temp_cookiefile)

        cookies = cookiejar.MozillaCookieJar()
        con = sqlite3.connect(temp_cookiefile)
        cur = con.cursor()
        cur.execute("""SELECT host, path, isSecure, expiry, name, value
        FROM moz_cookies""")
        for item in cur.fetchall():
            c = cookiejar.Cookie(
                0, item[4], item[5], None, False, item[0],
                item[0].startswith('.'), item[0].startswith('.'),
                item[1], False, item[2], item[3], item[3] == '', None,
                None, {},
            )
            cookies.set_cookie(c)

    else:
        log.e('[error] unsupported cookies format')
        # TODO: Chromium Cookies
        # SELECT host_key, path, secure, expires_utc, name, encrypted_value
        # FROM cookies
        # http://n8henrie.com/2013/11/use-chromes-cookies-for-easier-downloading-with-python-requests/

    return cookies


class Bilibiliests(unittest.TestCase):
    @patch('you_get.extractors.bilibili.cookies', None)
    def test_space_upload_video_no_cookie(self):
        bilibili.download('https://space.bilibili.com/357665034/', info_only=True)

    @patch('you_get.extractors.bilibili.cookies', load_cookies('E:/cookies.txt'))
    @patch('you_get.common.cookies', load_cookies('E:/cookies.txt'))
    def test_space_home(self):
        bilibili.download('https://space.bilibili.com/8047632/', info_only=True)

    @patch('you_get.extractors.bilibili.cookies', load_cookies('E:/cookies.txt'))
    @patch('you_get.common.cookies', load_cookies('E:/cookies.txt'))
    def test_space_upload_video(self):
        bilibili.download('https://space.bilibili.com/357665034/upload/video', info_only=True)

    @patch('you_get.extractors.bilibili.cookies', load_cookies('E:/cookies.txt'))
    @patch('you_get.common.cookies', load_cookies('E:/cookies.txt'))
    def test_space_upload_video_old(self):
        # bilibili.download('https://space.bilibili.com/8047632/video', info_only=True)
        bilibili.download('https://space.bilibili.com/347691691/video', info_only=True)

    def Stest_space_lists(self):
        bilibili.download('https://space.bilibili.com/254463269/lists', info_only=True, output_dir='.')

    def test_space_lists_old(self):
        bilibili.download('https://space.bilibili.com/254463269/channel/series', info_only=True, output_dir='.')

    def test_space_lists_series(self):
        bilibili.download('https://space.bilibili.com/8047632/lists/60489?type=series', info_only=True)

    def test_space_lists_series_old(self):
        bilibili.download('https://space.bilibili.com/8047632/channel/seriesdetail?sid=60489', info_only=True)

    def test_space_lists_season(self):
        bilibili.download('https://space.bilibili.com/8047632/lists/1308605?type=season', info_only=True)

    def test_space_lists_season_old(self):
        bilibili.download('https://space.bilibili.com/8047632/channel/collectiondetail?sid=1308605', info_only=True)


if __name__ == '__main__':
    unittest.main()
