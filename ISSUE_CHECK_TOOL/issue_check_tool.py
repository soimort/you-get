#!/usr/bin/env python3
'''
sorry, I don't know how to resolve this issue.
when I try to download a video that time is more than 90 mins from bilibili.com
everything is good, the video is also downloaded
But, the xml file is not good
the xml file only contain all things in 90 mins, but nothing after 90 mins
for example:
    I try to download this video(its time is more than 90 mins, and has danmu after 90 mins) https://www.bilibili.com/video/BV1j7411N7Dz 
    after you-get goes well, the downloaded vidieo is good except xml file is only containing all things that less than 90 mins, and xml file does not contain the any thing after 90 mins
I don't know the cid number about xml is good or not.
I wish you could help, good luck to you

当尝试从b站下载超过90分钟的视频的时候,视频下载是可以的.
但是随视频下载的xml文件 不会 包含超过90分钟后的弹幕资源
这是我使用you-get的时候遇到的问题

下面是我用来排序xml内容的脚本,可以用 https://www.bilibili.com/video/BV1j7411N7Dz 这个视频来测试,
可以看出xml中d标签中的时间字段最大值不会超过90(5400秒)分钟, 而这个视频在90分钟以后是还有字幕的
救救孩子吧, 祝你好运

'''
#
import parsel
import sys

def sort_key(str_str):
    compare_str = str_str.split(',')[0].replace('<d p="', '')
    return float(compare_str)

with open(sys.argv[1],'r') as f:
    tmp_xml = f.read()
    #print(tmp_xml)
    xml_xml = parsel.Selector(tmp_xml)
    xml_d_ = xml_xml.xpath('//d').getall()
    xml_d = sorted(xml_d_, key=sort_key)
    xml_str = ''
    for tmp_a in xml_d:
        #print(sort_key(tmp_a))
        xml_str = xml_str + str(tmp_a + '\n')
    xml_head = '''<?xml version="1.0" encoding="UTF-8"?><i><chatserver>chat.bilibili.com</chatserver><chatid>2648313</chatid><mission>0</mission><maxlimit>1500</maxlimit><source>k-v</source>''' + '\n'
    #xml_head = '''<?xml version="1.0" encoding="UTF-8"?><i>''' + '\n'
    xml_str = xml_head + xml_str + '''</i>'''
    with open('convert.xml', 'w') as f_f:
        f_f.write(xml_str)
