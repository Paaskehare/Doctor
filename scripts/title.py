#!/usr/bin/env python
# encoding: utf-8

import re
import html.parser
import json
from urllib.request import urlopen

import doctor
from doctor.hooks import pubmsg

MODULE_NAME = 'title'

TitlePattern = re.compile(b'<title.*>(.*?)<\/title>', re.I | re.S)
YouTubePattern = re.compile('http://(www\.)?youtube\.com/watch\?v=([a-zA-Z0-9\-_]{10,13})', re.I)

def title(url):
    page = None
    try:
        page = urlopen(url)
    except:
        return

    finally:
        try:
            match = TitlePattern.search(page.read())
            page.close()
            if match:
                title = match.groups(0)[0].decode('utf-8').strip().replace('\n', ' ').replace('\r', '')
                h = html.parser.HTMLParser()

                if title:
                    return h.unescape(title)
                else:
                    return
        except AttributeError:
            return

def youtube(id):
    try:
        try:
            url = 'http://gdata.youtube.com/feeds/videos/%s?alt=json' % id
            page = urlopen(url)
        finally:
            entry = json.loads(page.read().decode('utf-8'))['entry']
            vid = {'title': entry['title']['$t'], 'category': entry['media$group']['media$category'][0]['label']}
            page.close()
            return vid
    except:
        return


@doctor.hooks.pubmsg
def message(user, channel, msg):
  
  match = re.search(r'((http|ftp|https):\/\/[\w\-_]+(\.[\w\-_]+)+([\w\-\.,@?^=%&amp;:/~\+#]*[\w\-\@?^=%&amp;/~\+#])?)', msg)
  if match:
    url = match.groups(0)[0]

    result = ''

    yt = YouTubePattern.match(url)

    if yt:
      result = '(%s) %s' % youtube(yt.groups(0)[1])
    else:
      result = title(url)

    if result:
      bot.say(result, channel)
