#!/usr/bin/env python
# encoding: utf-8

from doctor import Doctor

options = {
  # IRC Networks to connect to
  'networks': [
    #{
    #  'host':     'irc.quakenet.org',
    #  'nick':     'Doctorious',
    #  'ident':    'bot',
    #  'channels': ['#ole', '#doctor',],
    #},
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
    'notify',
    'wolfram',
    'title',
  ],

  # Triggers the bot should treat as "commands"
  'trigger': ('!', '.',),

  # Prefix for all messages sent from the bot
  'prefix': '\x0310>\x0F '
}

if __name__ == '__main__':
    bot = Doctor(options)
    bot.run()
