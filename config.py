#!/usr/bin/env python

# Options
options = {
  # IRC Networks to connect to
  # TODO: Currently only supports a single network at a time, but uses an array for future implementation compatibility.
  'networks': [
    {
      'host':     'irc.quakenet.org',
      'nick':     'Doctorious',
      'ident':    'bot',
      'channels': ['#ole', '#doctor',], 
    },
  ],

  # Scripts to load on startup
  'scripts': [
    'auth',
    'example',
    'wolfram',
    'title',
  ],

  # Triggers the bot should treat as "commands"
  'trigger': ('!', '.',),

  # Default prefix for all messages sent from the bot
  'prefix': '\x034>\x0F '
}
