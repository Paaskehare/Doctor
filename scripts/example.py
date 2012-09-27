#!/usr/bin/env python
# encoding: utf-8

import doctor

@doctor.Alias('hey', 'yo', 'heya')
def command_hi(user, channel, message):
    channel.say("heya! %s" % message)
    channel.say("You are \x02{.nick}\x02".format(user))
