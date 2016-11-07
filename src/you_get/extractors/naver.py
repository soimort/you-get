#!/usr/bin/env python

__all__ = ['naver_download']
import urllib.request, urllib.parse
from ..common import *

def naver_download(url, output_dir = '.', merge = True, info_only = False, **kwargs):

	assert re.search(r'http://tvcast.naver.com/v/', url), "URL is not supported"

	html = get_html(url)
	contentid = re.search(r'var rmcPlayer = new nhn.rmcnmv.RMCVideoPlayer\("(.+?)", "(.+?)"',html)
	videoid = contentid.group(1)
	inkey = contentid.group(2)
	assert videoid
	assert inkey
	info_key = urllib.parse.urlencode({'vid': videoid, 'inKey': inkey, })
	down_key = urllib.parse.urlencode({'masterVid': videoid,'protocol': 'p2p','inKey': inkey, })
	inf_xml = get_html('http://serviceapi.rmcnmv.naver.com/flash/videoInfo.nhn?%s' % info_key )

	from xml.dom.minidom import parseString
	doc_info = parseString(inf_xml)
	Subject = doc_info.getElementsByTagName('Subject')[0].firstChild
	title = Subject.data
	assert title

	xml = get_html('http://serviceapi.rmcnmv.naver.com/flash/playableEncodingOption.nhn?%s' % down_key )
	doc = parseString(xml)

	encodingoptions = doc.getElementsByTagName('EncodingOption')
	old_height = doc.getElementsByTagName('height')[0]
	real_url= ''
	#to download the highest resolution one,
	for node in encodingoptions:
		new_height = node.getElementsByTagName('height')[0]
		domain_node = node.getElementsByTagName('Domain')[0]
		uri_node = node.getElementsByTagName('uri')[0]
		if int(new_height.firstChild.data) > int (old_height.firstChild.data):
			real_url= domain_node.firstChild.data+ '/' +uri_node.firstChild.data

	type, ext, size = url_info(real_url)
	print_info(site_info, title, type, size)
	if not info_only:
		download_urls([real_url], title, ext, size, output_dir, merge = merge)

site_info = "tvcast.naver.com"
download = naver_download
download_playlist = playlist_not_supported('naver')
