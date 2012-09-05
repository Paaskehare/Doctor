#!/usr/bin/env python
# encoding: utf-8

import config
import doctor

from doctor.irc import Network

if __name__ == '__main__':
    bot = Network('irc.freenode.org', 6667, 'Doctorious', channels=['#doctor'])
    bot.run()
