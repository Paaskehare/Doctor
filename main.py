#!/usr/bin/env python
# encoding: utf-8

import config
import doctor

from doctor.irc import Network
from doctor import Doctor

if __name__ == '__main__':
    bot = Doctor(config.options)
    bot.run()
