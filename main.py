#!/usr/bin/env python
# encoding: utf-8

import doctor

from doctor.irc import Network
from doctor import Doctor

options = {
  # IRC Networks to connect to
  'networks': [
    {
      'host':     'irc.quakenet.org',
      'nick':     'Doctorious',
      'ident':    'bot',
      'channels': ['#ole', '#doctor',],
    },
    {
      'host':     'irc.freenode.org',
      'nick':     'Doctorious',
      'channels': ['#doctor'],
    }
  ],

  # Scripts to load on startup
  'scripts': [
    'auth',
    'example',
    #'wolfram',
    #'title',
  ],

  # Triggers the bot should treat as "commands"
  'trigger': ('!', '.',),

  # Prefix for all messages sent from the bot
  'prefix': '\x034>\x0F '
}

if __name__ == '__main__':
    bot = Doctor(options)
    bot.run()
