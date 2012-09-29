#!/usr/bin/env python
# encoding: utf-8

import doctor

from urllib.request import urlopen
from urllib.parse import urlencode
import json

@doctor.Alias('u')
def command_urban(user, channel, args):
    if not args: return
    
    term = urlencode({'term': args})
    url = 'http://www.urbandictionary.com/iphone/search/define?' + term

    try:
        page = urlopen(url, timeout = 2.0)
        results = json.loads(page.read().decode('utf-8'))['list'][0]

        result['definition'] = result['definition'][:130]
        channel.say('Term: \x0310%(word)s\x0F Definition: \x0310%(definition)s\x0F' % result)
    except:
        channel.say('Does not compute')