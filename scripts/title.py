#!/usr/bin/env python
# encoding: utf-8

import re
import html.parser
import json
from urllib.request import urlopen

import doctor
from doctor import message

TitlePattern = re.compile(b'<title.*>(.*?)<\/title>', re.I | re.S)
YouTubePattern = re.compile('https?://(www\.)?(youtube\.com/.+(\?|&)v=|youtu\.be/)([a-zA-Z0-9\-_]{10,13})', re.I)
URLPattern = re.compile('((http|ftp|https):\/\/[\w\-_]+(\.[\w\-_]+)+([\w\-\.,@?^=%&amp;:/~\+#]*[\w\-\@?^=%&amp;/~\+#])?)', re.I)
MediaPattern = re.compile('(png|jpg|bmp|gif|avi|mpg|flv|3gp|mp4|exe|msi|mp3|flac|tar\.gz|tar\.bz2)$', re.I)

def read_page(url):
    page = b''
    try:    page =  urlopen(url, timeout = 2.0).read()
    except: pass
    return page

def title(url):
    youtube = YouTubePattern.match(url)

    if youtube:
        page = read_page('http://gdata.youtube.com/feeds/videos/%s?alt=json' % youtube.group(4)).decode('utf-8')
        result = json.loads(page)['entry']

        return '(\x034%s\x03) %s' % (
          result['media$group']['media$category'][0]['label'], 
          result['title']['$t']
        )
    else:
        if MediaPattern.match(url): return

        page = read_page(url)
        title = TitlePattern.search(page)
        
        if title:
            h = html.parser.HTMLParser()
            title = h.unescape(title.groups(0)[0].decode('utf-8')).strip().replace('\n', ' ').replace('\r', '')

            return title
        return

@message
def message(network, user, channel, msg):
    match = re.search(URLPattern, msg)
    if match:
        url = match.groups(0)[0]
        text = title(url)

        if text:
            channel.say(text)

