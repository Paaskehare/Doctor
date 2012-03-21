#!/usr/bin/env python

from doctor import Client
import config

if __name__ == '__main__':
  try:
    bot = Client(config.nick, config.server, config.channels)
  except KeyboardInterrupt:
    print('Shutting down')
