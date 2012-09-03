#!/usr/bin/env python
# encoding: utf-8

import doctor
from doctor.hooks import message
from doctor.script import Alias

@Alias('hey', 'yo', 'heya')
def command_hi(user, channel, message):
    channel.say("heya! %s" % message)
    channel.say("You are {.nick}".format(user))
