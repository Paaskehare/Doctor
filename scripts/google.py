#!/usr/bin/env python
# encoding: utf-8

import doctor
import json
from urllib.request import urlopen
from urllib.parse  import urlencode

from html.parser import HTMLParser

@doctor.alias('g')
def command_google(user, channel, message):
  try:
    query = urlencode({'q': ' '.join(message)})
    page = urlopen('http://ajax.googleapis.com/ajax/services/search/web?v=1.0&' + query)
    result = json.loads(page.read().decode('utf-8'))['responseData']['results'][0]

    result['titleNoFormatting'] = HTMLParser().unescape(result['titleNoFormatting'])
    channel.say('Google: \x0310%(titleNoFormatting)s\x03 - %(unescapedUrl)s' % result)
  except:
    channel.say('No results returned.')