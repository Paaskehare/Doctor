hooks = {}

def create_or_append(event, call):
  global hooks
  if event in hooks:
    hooks[event].append(call)
  else:
    hooks[event] = [call]

def hookable(target, *args, **kwargs):
  global hooks

  def wrapper(*args, **kwargs):
    e = args[-1]
    if e.eventtype() in hooks:
      for hook in hooks[e.eventtype()]:
        hook(e.source(), e.target(), e.arguments()[0])
    return target(*args, **kwargs)
  return wrapper

class pubmsg:
  def __init__(self, f):
    global hooks
    create_or_append('pubmsg', f)

class welcome:
  def __init__(self, f):
    global hooks
    create_or_append('welcome', f)
