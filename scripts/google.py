#!/usr/bin/env python
# encoding: utf-8

MODULE_NAME = 'google'
import json
from urllib.request import urlopen
from urllib.parse import urlencode

from html.parser import HTMLParser

def command_g(user, channel, args):
  command_google(user, channel, args)

def command_google(user, channel, arguments):
  try:
    query = urlencode({'q': ' '.join(arguments[1:])})
    page = urlopen('http://ajax.googleapis.com/ajax/services/search/web?v=1.0&' + query)
    result = json.loads(page.read().decode('utf-8'))['responseData']['results'][0]
    h = HTMLParser()

    result['titleNoFormatting'] = h.unescape(result['titleNoFormatting'])
    bot.say('Google: %(titleNoFormatting)s - %(unescapedUrl)s' % result, channel)
  except:
    bot.say('No results returned.', channel)
