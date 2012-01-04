#!/usr/bin/env python
# encoding: utf-8

MODULE_NAME = 'urban'
from urllib.request import urlopen
from urllib.parse import urlencode
import json

def command_urban(user, channel, args):
  term = urlencode({'term': args[1]})
  url = 'http://www.urbandictionary.com/iphone/search/define?' + term

  try:
    page = urlopen(url)
    result = json.loads(page.read().decode('utf-8'))['list'][0]

    result['definition'] = result['definition'][:130]
    bot.say('Term: %(word)s Definition: %(definition)s' % result, channel)
  except:
    bot.say('Does not compute', channel)
