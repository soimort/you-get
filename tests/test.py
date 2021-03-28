#!/usr/bin/env python

import unittest

from you_get.extractors import (
    imgur,
    magisto,
    youtube,
    missevan,
    acfun,
    bilibili,
    soundcloud,
    tiktok
)


class YouGetTests(unittest.TestCase):

    def test_music163(self):
        ## single song
        music163.download('https://music.163.com/#/song?id=351116', info_only=True)

        
        ## playlist
        #soundcloud.download(
        #    'https://soundcloud.com/anthony-flieger/sets/cytus', info_only=True
        #)



if __name__ == '__main__':
    unittest.main()
