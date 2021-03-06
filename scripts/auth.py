import doctor

admins = (
  'ole!~ole@ole.im',
)

def command_unload(user, channel, args):
    if is_authorized(user):
        for arg in args.split():
            doctor.script_manager.unload(arg)

def command_load(user, channel, args):
    if is_authorized(user):
        for arg in args.split():
            doctor.script_manager.load(arg)
 

def command_reload(user, channel, args):
    if is_authorized(user):
        doctor.script_manager.reload()
        channel.say('Reloaded.')
    else:
        channel.say('You cant issue that command')

def command_flags(user, channel, args):
    channel.say('You are {.nick} and have the flags {.flags}'.format(user, user))

def is_authorized(user):
    return '{.nick}!{.ident}@{.host}'.format(user, user, user) in admins
