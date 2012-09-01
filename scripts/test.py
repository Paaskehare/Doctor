#!/usr/bin/env python
# encoding: utf-8

import doctor
from doctor.hooks import message

def command_hi(user, channel, msg):
    channel.say("heya! %s" % msg)
    channel.say("You are {.nick}".format(user))

@message
def message(network, user, channel, args):
    channel.say('got a message!')
