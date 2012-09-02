#!/usr/bin/env python
# encoding: utf-8

import doctor
from doctor.hooks import message

def command_hi(user, channel, message):
    channel.say("heya! %s" % message)
    channel.say("You are {.nick}".format(user))

@message
def message(network, user, channel, message):
    reply = '{.nick} said {}'.format(user, args)
    channel.say(reply)
