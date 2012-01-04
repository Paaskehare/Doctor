MODULE_NAME = 'example'

def command_test(user, channel, args):
  bot.say('You wrote: %s' % ' '.join(args[1:]), channel)
