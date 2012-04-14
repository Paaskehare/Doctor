import doctor

def create_or_append(event, call):
  if event in doctor.hooks:
    doctor.hooks[event].append(call)
  else:
    doctor.hooks[event] = [call]

def hookable(target, *args, **kwargs):

  def wrapper(*args, **kwargs):
    e = args[-1]
    if e.eventtype() in doctor.hooks:
      for hook in doctor.hooks[e.eventtype()]:
        hook(e.source(), e.target(), e.arguments()[0])
    return target(*args, **kwargs)
  return wrapper

class Hook:
  def __init__(self, f):
    create_or_append(self.__class__.__name__, f)

class pubmsg(Hook): pass
class welcome(Hook): pass
