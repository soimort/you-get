#!/usr/bin/env python

__all__ = ['ehow_download']

from ..common import *

def ehow_download(url, output_dir = '.', merge = True, info_only = False, **kwargs):
	
	assert re.search(r'http://www.ehow.com/video_', url), "URL you entered is not supported"

	html = get_html(url)
	contentid = r1(r'<meta name="contentid" scheme="DMINSTR2" content="([^"]+)" />', html)
	vid = r1(r'"demand_ehow_videoid":"([^"]+)"', html)
	assert vid

	xml = get_html('http://www.ehow.com/services/video/series.xml?demand_ehow_videoid=%s' % vid)
    
	from xml.dom.minidom import parseString
	doc = parseString(xml)
	tab = doc.getElementsByTagName('related')[0].firstChild

	for video in tab.childNodes:
		if re.search(contentid, video.attributes['link'].value):
			url = video.attributes['flv'].value
			break

	title = video.attributes['title'].value
	assert title 

	type, ext, size = url_info(url)
	print_info(site_info, title, type, size)
	
	if not info_only:
		download_urls([url], title, ext, size, output_dir, merge = merge)

site_info = "ehow.com"
download = ehow_download
download_playlist = playlist_not_supported('ehow')
