#!/usr/bin/env python
# encoding: utf-8

import config
import doctor

from doctor.irc import Network

if __name__ == '__main__':
    bot = Network('+irc.freenode.org', 6697, "Doctorious", channels=['#ole', '#monkeytime'])
    bot.identify()
    bot.run()
