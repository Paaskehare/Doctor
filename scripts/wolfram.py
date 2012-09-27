#!/usr/bin/env python
# encoding: utf-8

from urllib.request import urlopen
from urllib.parse import urlencode
from xml.etree import ElementTree as etree

MODULE_NAME = 'calc'

def wolfram(expression):
  query = urlencode(
    {
      'format': 'plaintext',
      'input': expression,
      'appid': 'QVAAPJ-RVP9X4RQJY',
      'timeout': '1',
    }
  )

  url = 'http://api.wolframalpha.com/v2/query?' + query

  page = urlopen(url)
  tree = etree.parse(page)
  root = tree.getroot()
    
  if root.attrib['success'] == 'true':
    return {
      'question': root[0][0][0].text,
      'answer': root[1][0][0].text
    }
  return

def command_calc(user, channel, arguments):
  result = wolfram(arguments)

  if result:
    channel.say('%(question)s \x034=\x03 %(answer)s' % result)
  else:
    channel.say('No result')
