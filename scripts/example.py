#!/usr/bin/env python
# encoding: utf-8

import doctor

cache = doctor.Storage('example')

# example of initiating a simple storage object:
if not cache.messages:
    cache.messages = {}

@doctor.Alias('hej', 'yo', 'heya')
def command_hi(user, channel, message):
    channel.say("Hey! You are \x02{.nick}\x02".format(user))

    # example of using a simple storage object:
    msg = cache.messages.get(user.nick, '')
    if msg:
        channel.say('I stored your message from last time!')
        channel.say(msg)
    cache.messages[user.nick] = message
