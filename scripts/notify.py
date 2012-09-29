#!/usr/bin/env python
import doctor
from time import time

cache = doctor.Storage('notify')

if not cache.notes: cache.notes = {}

def time_since(timestamp):
    now = int(time())

    minute = 60
    hour   = 60  * minute
    day    = 24  * hour
    week   = 7   * day

    if now < timestamp + minute:
        return 'less than a minute ago'

    elif now > timestamp + minute and now < timestamp + hour:
        stamp = int((now - timestamp) / minute)
        return '%s minute%s ago' % ((stamp, '' if stamp == 1 else 's'))

    elif now < timestamp + day:
        stamp = int((now - timestamp) / hour)
        return '%s hour%s ago' % ((stamp, '' if stamp == 1 else 's'))

    elif now < timestamp + (week * 4):
        stamp = int((now - timestamp) / day)
        return '%s day%s ago' % ((stamp, '' if stamp == 1 else 's'))

    stamp = int((now - timestamp) / week)
    return '%s weeks ago' % stamp

def note_add(user, nick, message):
    note = {
      'from': user.nick,
      'message': message,
      'time': int(time()),
    }

    if cache.notes.get(nick, None):
        cache.notes[nick].append(note)
    else:
        cache.notes[nick] = [note]

def notes_for(nickname, channel):
    notes = cache.notes.get(nickname, [])
    if notes:
        for note in notes:
            msg = '\x0310%s\x0F - \x02%s\x02 left a message a message for you "\x0310%s\x0F" %s' % (
                nickname, note['from'], note['message'], time_since(note['time'])
            )
            channel.say(msg)
        del cache.notes[nickname]

@doctor.message
def message(network, user, channel, msg):
    notes_for(user.nick, channel)

@doctor.user_joined
def user_joined(network, user, channel):
    notes_for(user.nick, channel)

@doctor.user_rename
def user_rename(network, user, channel, old_nick):
    notes_for(user.nick, channel)
    notes_for(old_nick, channel)

def command_notify(user, channel, message):
    nick, *msg = message.split()

    if msg:
        note_add(user, nick, ' '.join(msg))
        channel.say('Notification stored.')
