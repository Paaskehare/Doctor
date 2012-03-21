#!/usr/bin/python
# coding: utf-8

server = 'irc.freenode.org', 6667

# For password use either None, 'password', or 'username:password'
password = None

# Use SSL?
use_ssl = False


# Nickname of the bot
nick = 'Doctor23'
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

# Bot Line prefix
prefix = '\x034>\x0F '

# Command triggers
trigger = '!', '.'
