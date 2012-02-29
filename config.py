#!/usr/bin/python
# coding: utf-8

server = 'irc.freenode.org', 6667

# for password use either None, 'password', or 'username:password'
password = None
usessl = False


# Nickname of the bot
nick = 'Doctor'
realname = nick

# List of channels to join on connect
channels = [
  '#ole',
]

# Plugins to load at startup
scripts = [
  'calc',
  'urban',
  'google',
  'example',
  'title',
]


prefix = '\x034>\x0F '

trigger = '!', '.'
