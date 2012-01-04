#!/usr/bin/env python
# encoding: utf-8

import re
import sys
try:
  import scripts
except ImportError:
  pass

class ScriptManager:
  def __init__(self, bot, scripts):
    self.bot = bot
    for script in scripts:
      self.load(script)

  def serialize(self, name):
    return re.sub(r'[^a-z]', '', name.lower())

  def load(self, script):
    script = self.serialize(script)
    try:
      print('* Successfully imported ', script)
      mod = __import__('scripts.'+script, {}, {}, ['mod'], 0)
      mod.bot = self.bot
      try: mod._init()
      except: pass
      for func in dir(mod):
        if func.startswith('command_'):
          self.bot.commands[func[len('command_'):]] = getattr(mod, func)
    except:
      print('import error')
      pass

  def unload(self, script):
    script = self.serialize(script)
    mod = 'scripts.' + script
    print(mod)
    try:
      print(dir(sys.modules[mod]))
      for func in dir(sys.modules[mod]):
        if func.startswith('command'):
          del self.bot.commands[func[len('command_'):]]
      del sys.modules[mod]
    except:
      pass

  def reload(self, script):
    self.unload(script)
    self.load(script)
